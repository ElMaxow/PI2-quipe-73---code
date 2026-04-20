from machine import Pin, PWM
import time
from time import sleep

#c = 0.95 #correction gauche droite
#d = 1

IN_2 = Pin(27, Pin.OUT)
IN_3 = Pin(26, Pin.OUT)
led_b = Pin(2, Pin.OUT)
IN_2.off()
IN_3.off()
# laisser ça après, sinon il y a un kick dans les moteurs - Max
IN_2 = PWM(Pin(27), freq=1000)  # PWM droite
IN_3 = PWM(Pin(26), freq=1000)  # PWM gauche
IN_2.duty(0)
IN_3.duty(0)
IN_1 = PWM(Pin(18), freq=1000)  # PWM droite
IN_4 = PWM(Pin(25), freq=1000)  # PWM gauche
IN_1.duty(0)
IN_4.duty(0)


def avancer(vitesse=800, c = 1, d = 0.95):
    led_b.on()
    IN_2.duty(0)
    IN_3.duty(0)
    IN_1.duty(int(vitesse*d)) # 0.85 sweet spot
    IN_4.duty(int(vitesse*c))
    
 
def stop():
    led_b.off()
    IN_2.duty(0)
    IN_3.duty(0)
    IN_1.duty(0)
    IN_4.duty(0)

def droite(vitesse=600, c= 1, d = 0.95):
    led_b.on()
    IN_2.duty(int(vitesse*d))
    IN_3.duty(0)
    IN_1.duty(0)
    IN_4.duty(int(vitesse*c))
    
def gauche(vitesse=600, c = 1, d = 0.95):
     led_b.on()
     IN_2.duty(0)
     IN_3.duty(int(vitesse*c))
     IN_1.duty(int(vitesse*d))
     IN_4.duty(0)

"""
def droite(vitesse=700, facteur=0.60, c=0.95): # virage doux à droite, sans tourner sur place
#     led_b.on()
    IN_2.duty(0)
    IN_3.duty(0) # une roue tourne moins vite que l'autre
    IN_1.duty(int(vitesse * facteur * c))
    IN_4.duty(vitesse)
    
def gauche(vitesse=700, facteur=0.60, c=0.95): # virage doux à gauche, sans tourner sur place
#     led_b.on()
    IN_2.duty(0)
    IN_3.duty(0)
    IN_1.duty(int(vitesse * c))
    IN_4.duty(int(vitesse * facteur))
"""

def reculer(vitesse=800, c = 1, d = 0.95):
    led_b.on()
    IN_2.duty(int(vitesse*d))
    IN_3.duty(int(vitesse*c))
    IN_1.duty(0) # 0.85 sweet spot
    IN_4.duty(0)

"""

def tourner_sur_place(vitesse=600):
    print("tourne sur place")
#     led_b.on()
    IN_1.duty(0)
    IN_4.duty(vitesse)
    IN_2.duty(vitesse)
    IN_3.duty(0)
"""



# test
"""
avancer(800)
print("go")
time.sleep(2)
stop()
"""
