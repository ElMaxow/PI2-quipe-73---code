from mouv import avancer, stop, droite, gauche, reculer
from time import sleep, time
from enco import distance_gauche, distance_droite, reset, distance_moyenne
from temps import temps
from gyro import reset_angle, get_angle

# ajuster position :
temps_max = 100
def correction(Kp=0.02):  # ⚠️ petit gain au début
    erreur = distance_gauche() - distance_droite()
    
    correction = Kp * erreur
    
    c = 1 - correction
    d = 1 + correction
    
    # LIMITES SAFE (important)
    c = max(0.9, min(1.1, c))
    d = max(0.9, min(1.1, d))
    
    return c, d

def ajuster_position(delta = 0.5, distance_max = 5, attendre = 0.5):
    distance_ini = distance_moyenne()
    distance_max = distance_ini + distance_max
    if distance_droite() - distance_gauche() >= delta:
        while distance_droite() - distance_gauche() >= delta and temps() < temps_max and distance_moyenne() < distance_max:
            avancer(1023, 1, 0.5)
            #print(distance_droite() - distance_gauche())
            sleep(0.1)
    elif distance_gauche() - distance_droite() >= delta:
        while distance_gauche() - distance_droite() >= delta and temps() < temps_max and distance_moyenne() < distance_max:
            avancer(1023, 0.5, 1)
            #print(distance_gauche() - distance_droite())
            sleep(0.1)
    stop()
    sleep(attendre)
    
def avancer_de(cm = 50, attendre = 0.5):
    reset()
    
    base_speed = 800   # un peu moins que 900 pour stabilité
    
    while abs(distance_moyenne()) < cm and temps() < temps_max:
        
        c, d = correction()   # ← ICI tu récupères la correction
        
        avancer(base_speed, c, d)   # ← ICI tu l’appliques
        
        #print("dist:", distance_moyenne(), "err:", distance_gauche()-distance_droite())
        print(distance_droite(), distance_gauche())
        sleep(0.05)
    
    stop()
    sleep(attendre)
# 
# def avancer_de(cm = 50, attendre = 0.5):
#     reset()
#     while abs(distance_moyenne()) <cm and temps() < temps_max :
#         avancer(900, 1, 1)
#         print(distance_moyenne())
#         sleep(0.1)
#     stop()
#     sleep(attendre)

def reculer_de(cm = 50, attendre = 0.5):
    reset()
    while abs(distance_moyenne()) <cm and temps() < temps_max :
        reculer(1023, 1, 1)
        #print(distance_moyenne())
        sleep(0.1)
    stop()
    sleep(attendre)

def tourner_gauche_de(angle = 90, attendre = 0.5):
    reset_angle()
    a = get_angle()
    while a <= angle and temps() < temps_max :
        gauche(1023, 1, 1)
        #print(a)
        sleep(0.1)
        a = get_angle()
    stop()
    sleep(attendre)

def tourner_droite_de(angle = 90, attendre = 0.5):
    reset_angle()
    a = get_angle()
    #print(a)
    #print(a >= angle)
    while a >= -angle and temps() < temps_max :
        droite(900, 1, 1)
        #print(a)
        sleep(0.1)
        a = get_angle()
    stop()
    sleep(attendre)




 