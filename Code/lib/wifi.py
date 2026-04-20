import network
import socket
import time
 
# ── Point d'accès WiFi ─────────────────────────────────────
ap = network.WLAN(network.AP_IF)
ap.active(False)
time.sleep(1)
ap.active(True)
ap.config(essid="Chien robot", password="12345678", authmode=3)
 
timeout = 10
while not ap.active() and timeout > 0:
    time.sleep(0.5)
    timeout -= 1
print("IP:", ap.ifconfig()[0])
 
# ── Page HTML ──────────────────────────────────────────────
HTML = b"""<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Robot</title>
<style>
body{margin:0;display:flex;flex-direction:column;align-items:center;
     justify-content:center;min-height:100vh;background:#111;}
h2{color:#fff;letter-spacing:2px;}
.grid{display:grid;grid-template-columns:repeat(3,80px);
      grid-template-rows:repeat(3,80px);gap:12px;margin-top:24px;}
.customs{display:flex;gap:12px;margin-top:24px;}
button{width:80px;height:80px;font-size:28px;border:none;
       border-radius:16px;background:#222;color:#fff;cursor:pointer;}
button:active{background:#0af;}
.custom-btn{font-size:14px;font-weight:500;letter-spacing:1px;
            background:#1a1a2e;border:1px solid #0af;}
#log{margin-top:24px;color:#0af;font-size:14px;letter-spacing:1px;}
 
/* ── Panneau temps / pwm / c ── */
.params{display:flex;gap:16px;align-items:flex-end;margin-top:28px;flex-wrap:wrap;justify-content:center;}
.params label{color:#aaa;font-size:12px;letter-spacing:1px;
              display:flex;flex-direction:column;gap:6px;}
.params input{width:90px;padding:8px;font-size:16px;text-align:center;
              background:#1a1a2e;color:#fff;border:1px solid #0af;
              border-radius:10px;outline:none;}
.send-btn{width:100px;height:44px;font-size:13px;font-weight:600;
          letter-spacing:1px;background:#0af;color:#000;border:none;
          border-radius:10px;cursor:pointer;}
.send-btn:active{background:#08c;}
</style></head><body>
<h2>ROBOT CONTROL</h2>
<div class="grid">
  <div></div>
  <button onclick="go('forward')">&#9650;</button>
  <div></div>
  <button onclick="go('left')">&#9668;</button>
  <button onclick="go('stop')" style="font-size:13px;">STOP</button>
  <button onclick="go('right')">&#9658;</button>
  <div></div>
  <button onclick="go('backward')">&#9660;</button>
  <div></div>
</div>
<div class="customs">
  <button class="custom-btn" onclick="go('custom1')">Queue</button>
  <button class="custom-btn" onclick="go('custom2')">LED</button>
  <button class="custom-btn" onclick="go('custom3')">Bouche</button>
</div>
 
<!-- ── Champs Temps + PWM + C ── -->
<div class="params">
  <label>TEMPS (à venir)
    <input type="number" id="temps" min="0" step="0.1" value="1">
  </label>
  <label>Vitesse (0-1023)
    <input type="number" id="pwm" min="0" max="1023" step="1" value="800">
  </label>
  <label>CORRECTION (0-1)
    <input type="number" id="c" min="0" max="1" step="0.01" value="1.00">
  </label>
  <button class="send-btn" onclick="sendParams()">ENVOYER</button>
</div>
 
<div id="log">Connecte...</div>
<script>
function getParams(){
  return {
    temps : document.getElementById('temps').value,
    pwm   : document.getElementById('pwm').value,
    c     : document.getElementById('c').value
  };
}
 
function go(cmd){
  var p = getParams();
  var x = new XMLHttpRequest();
  x.open('GET','/cmd?v='+cmd+'&temps='+p.temps+'&pwm='+p.pwm+'&c='+p.c, true);
  x.onload=function(){document.getElementById('log').textContent='> '+x.responseText;};
  x.send();
}
 
function sendParams(){
  var p = getParams();
  var x = new XMLHttpRequest();
  x.open('GET','/cmd?v=params&temps='+p.temps+'&pwm='+p.pwm+'&c='+p.c, true);
  x.onload=function(){document.getElementById('log').textContent='> '+x.responseText;};
  x.send();
}
</script></body></html>"""
 
# ── Serveur ────────────────────────────────────────────────
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
s.settimeout(None)
print("Serveur pret sur http://192.168.4.1")
 
_cmd_callback = None
 
def set_callback(fn):
    global _cmd_callback
    _cmd_callback = fn
 
def handle(conn):
    try:
        req = b""
        conn.settimeout(3.0)
        while True:
            chunk = conn.recv(128)
            if not chunk:
                break
            req += chunk
            if b"\r\n\r\n" in req:
                break
        req = req.decode("utf-8", "ignore")
 
        if "/cmd?v=" in req:
            qs = req.split("/cmd?")[1].split(" ")[0].strip()
            params = {}
            for part in qs.split("&"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    params[k] = v
            cmd = params.get("v", "")
 
            if cmd == "params":
                temps = params.get("temps", "?")
                pwm   = params.get("pwm",   "?")
                c     = params.get("c",     "?")
                print("temps =", temps, "s  |  pwm =", pwm, "  |  c =", c)
                label = "temps=" + temps + "s  pwm=" + pwm + "  c=" + c
            else:
                labels = {
                    "forward":  "Avance !",
                    "backward": "Recule !",
                    "left":     "Gauche !",
                    "right":    "Droite !",
                    "stop":     "Stop !",
                    "custom1":  "Commande 1",
                    "custom2":  "Commande 2",
                    "custom3":  "Commande 3",
                }
                label = labels.get(cmd, "?")
 
            if _cmd_callback:
                reponse = _cmd_callback(cmd, label, params)
                if reponse:
                    label = reponse
 
            resp = label.encode()
            conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
                      b"Connection: close\r\nContent-Length: " +
                      str(len(resp)).encode() + b"\r\n\r\n" + resp)
        else:
            conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
                      b"Connection: close\r\nContent-Length: " +
                      str(len(HTML)).encode() + b"\r\n\r\n" + HTML)
    except Exception as e:
        print("Erreur handle:", e)
    finally:
        conn.close()
 
def start():
    premier = True
    while True:
        try:
            conn, addr = s.accept()
            if premier:
                print("Client connecte :", addr)
                premier = False
            handle(conn)
        except Exception as e:
            print("Erreur accept:", e)
            time.sleep(0.1)