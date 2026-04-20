import wifi
from mouv import avancer, stop, droite, gauche, reculer
from time import sleep
from queu import queue
from enco import distance_gauche, distance_droite, reset
from blink import led
from depo import placer_jouet
import _thread as asynchrone


# ── Callback : reçoit chaque commande du site ──────────────
def on_commande(cmd, label_defaut, params=None):
    if params is None:
        params = {}
    t   = float(params.get("temps", 1))    # défaut : 1 seconde
    pwm = int(params.get("pwm", 1023))     # défaut : 1023
    d   = float(params.get("c", 0.95))
    c = 1

    if cmd == "forward":
        print("→ Action : moteurs EN AVANT")
        avancer(pwm, c, d)
        return "%.1f cm | %.1f cm" % (distance_gauche(), distance_droite())

    elif cmd == "backward":
        print("→ Action : moteurs EN ARRIERE")
        reculer(pwm, c, d)
        return "%.1f cm | %.1f cm" % (distance_gauche(), distance_droite())

    elif cmd == "left":
        print("→ Action : tourner GAUCHE")
        gauche(pwm, c, d)
        return "%.1f cm | %.1f cm" % (distance_gauche(), distance_droite())

    elif cmd == "right":
        print("→ Action : tourner DROITE")
        asynchrone.start_new_thread(droite, (pwm, c, d))
        return "%.1f cm | %.1f cm" % (distance_gauche(), distance_droite())

    elif cmd == "stop":
        print("→ Action : STOP moteurs")
        asynchrone.start_new_thread(stop, ())
        reset()
        return "Stop !"
    
    elif cmd == "custom1":
        print("wouf wouf")
        asynchrone.start_new_thread(queue, ())
        return "Wouf wouf !"

    elif cmd == "custom2":
        print("Que lumière soit")
        asynchrone.start_new_thread(led, ())
        return "Que lumière soit"

    elif cmd == "custom3":
        print("→ Action custom 3")
        asynchrone.start_new_thread(placer_jouet, ())
        return "Jouet placé"
    
    print(params)

    return label_defaut   # retourne le label par défaut pour les autres boutons

# ── Lancement ──────────────────────────────────────────────
def wifi_start():
    print("je suis la")
    wifi.set_callback(on_commande)
    wifi.start()   # boucle infinie, doit être en dernier