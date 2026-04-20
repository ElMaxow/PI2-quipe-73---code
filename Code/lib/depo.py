from machine import Pin, PWM
import time

servo2 = PWM(Pin(13), freq=50)  # servo sur GPIO 18

def set_angle(angle):
    duty = int(26 + (angle/180)*102)  # conversion angle -> PWM
    servo2.duty(duty)

def placer_jouet():
    angle = 45
    set_angle(float(angle))
    time.sleep(2)
    angle = 2
    set_angle(float(angle))
    time.sleep(1)
    
def fermer_bouche():
    set_angle(float(2))
    

#placer_jouet()