from mouv import avancer, stop, droite, gauche, reculer
from time import sleep, time
from queu import queue, queue_ini
from enco import distance_gauche, distance_droite, reset, distance_moyenne
from blink import led
from depo import placer_jouet, fermer_bouche
import _thread as asynchrone
from temps import temps, reset_time
from intelligent import ajuster_position, avancer_de, tourner_gauche_de, tourner_droite_de, reculer_de
from bouche import fermer_bouche, ouvrir_bouche
from placer_jouet import bouche_ini

"""
avancer(pwm, c, d)
"""

def lets_go(bouche_deb = False):
    print("go")
    reset_time()
    queue_ini()
    if bouche_deb == True :
        print("on ouvre la bouche")
        bouche_ini()
        
    fermer_bouche()
    sleep(0.5)
    # 1) avance vers cercle rouge
    avancer_de(cm = 64)
    print(distance_moyenne())

    # 1.1) ajuster position
    #ajuster_position(delta = 0.5, distance_max = 5)
    print(distance_gauche() - distance_droite())

    # 2) tourne un peu à gauche pour direction cercle bleu
    tourner_gauche_de(angle=45)

    # 3) avance vers bleu
    avancer_de(cm = 9)
    print(distance_moyenne())

    # 3.1) ajuster position
    #ajuster_position(delta = 0.2, distance_max = 3)
    #print(distance_gauche() - distance_droite())

    # 4) ouvrir bouche
    ouvrir_bouche()
    sleep(1.5)
    reculer_de(cm=5)
    sleep(0.5)
    fermer_bouche()
    
    # 4) reculer
    reculer_de(cm=8)
    print(distance_moyenne())

    # 5) pointer vers la fille
    tourner_gauche_de(angle=90-15)

    # Cligner de la DEL
    led()
    
    # 5) tourner
    tourner_droite_de(angle=57-15)

    # 7) avancer vers deuxième cercle rouge
    avancer_de(cm = 133)
    print(distance_moyenne())
    #ajuster_position(delta = 0.2, distance_max = 5)
    print(distance_gauche() - distance_droite())

    # 8 tourner vers la fille
    tourner_gauche_de(angle=135)

    # 9 Battre de la queue 3x
    queue()
    
    # 10 attendre 20 seconde
    sleep(20)
    
    # 11 tourner vers le troisième cerlce
    tourner_droite_de(angle=55)
    
    # 12 avacner vers le troisième cerlce
    avancer_de(cm = 60)
    print(distance_moyenne())
    #ajuster_position(delta = 0.2, distance_max = 4)

    # 2) tourner sur lui même (pas vers la fille)
    tourner_gauche_de(angle=360, attendre = 0.2)

    # 3) vers la fille
    tourner_gauche_de(angle=75)

#lets_go()