from machine import Pin, Timer
import time

# --- Compteurs et variables globales ---
ticks_gauche = 0
ticks_droit = 0


# Horodatage du dernier calcul de vitesse (en ms)
last_time_g = 0
last_time_d = 0
last_ticks_g = 0
last_ticks_d = 0

# --- Constantes à adapter à votre matériel ---
TICKS_PAR_TOUR = 360    # Nombre de ticks par tour complet de roue ; vérifié par Max
CIRCONF_CM = 3.14159 * 4.056 * 1.2 #1.2 correction test reel - Max

# -----------------------------------------------
# HANDLERS D'INTERRUPTION
# -----------------------------------------------

def count_g(pin):
    """Interruption sur canal A gauche : lit B pour déterminer le sens."""
    global ticks_gauche
    if enc_gauche_b.value() == 0:
        ticks_gauche += 1   # Sens avant
    else:
        ticks_gauche -= 1   # Sens arrière

def count_d(pin):
    """Interruption sur canal A droit : lit B pour déterminer le sens."""
    global ticks_droit
    if enc_droit_b.value() == 0:
        ticks_droit += 1    # Sens avant
    else:
        ticks_droit -= 1    # Sens arrière

# -----------------------------------------------
# INITIALISATION
# -----------------------------------------------

def init():
    """Configure les pins et attache les interruptions."""
    global enc_gauche_a, enc_gauche_b
    global enc_droit_a,  enc_droit_b

    # Canal A  → déclenche l'interruption
    # Canal B  → lu dans le handler pour connaître le sens
    enc_gauche_a = Pin(23, Pin.IN)
    enc_gauche_b = Pin(17, Pin.IN)

    enc_droit_a  = Pin(35, Pin.IN)
    enc_droit_b  = Pin(14, Pin.IN)

    # Interruption uniquement sur le front montant du canal A
    enc_gauche_a.irq(trigger=Pin.IRQ_RISING, handler=count_g)
    enc_droit_a.irq( trigger=Pin.IRQ_RISING, handler=count_d)

# -----------------------------------------------
# FONCTIONS UTILITAIRES
# -----------------------------------------------

def ticks_vers_cm(ticks):
    """Convertit un nombre de ticks en centimètres parcourus."""
    return (ticks / TICKS_PAR_TOUR) * CIRCONF_CM

def distance_gauche():
    """Retourne la distance parcourue par la roue gauche (en cm).
    Valeur négative = recul."""
    return ticks_vers_cm(ticks_gauche)

def distance_droite():
    """Retourne la distance parcourue par la roue droite (en cm).
    Valeur négative = recul."""
    return ticks_vers_cm(ticks_droit)

def distance_moyenne():
    """Retourne la distance moyenne des deux roues (en cm)."""
    return (abs(distance_gauche()) + abs(distance_droite())) / 2

def vitesse_gauche():
    """Retourne la vitesse instantanée de la roue gauche (cm/s)."""
    global last_time_g, last_ticks_g
    now = time.ticks_ms()
    dt_ms = time.ticks_diff(now, last_time_g)
    if dt_ms == 0:
        return 0.0
    dt_ticks = ticks_gauche - last_ticks_g
    last_time_g  = now
    last_ticks_g = ticks_gauche
    return ticks_vers_cm(dt_ticks) / (dt_ms / 1000.0)

def vitesse_droite():
    """Retourne la vitesse instantanée de la roue droite (cm/s)."""
    global last_time_d, last_ticks_d
    now = time.ticks_ms()
    dt_ms = time.ticks_diff(now, last_time_d)
    if dt_ms == 0:
        return 0.0
    dt_ticks = ticks_droit - last_ticks_d
    last_time_d  = now
    last_ticks_d = ticks_droit
    return ticks_vers_cm(dt_ticks) / (dt_ms / 1000.0)

def reset():
    """Remet tous les compteurs et horodatages à zéro."""
    global ticks_gauche, ticks_droit
    global last_time_g, last_time_d, last_ticks_g, last_ticks_d
    ticks_gauche = ticks_droit = 0
    last_ticks_g = last_ticks_d = 0
    last_time_g  = last_time_d  = time.ticks_ms()

init()  

"""
init()  
while True :
    print(distance_droite(), ticks_gauche, ticks_droit)
    time.sleep(1)
    
"""