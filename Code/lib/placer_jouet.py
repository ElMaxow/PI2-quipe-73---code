from machine import Pin, PWM
import time

servo = PWM(Pin(13), freq=50)  # servo sur GPIO 13

def set_angle(angle):
    duty = int(26 + (angle / 180) * 102)  # conversion angle -> PWM
    servo.duty(duty)


def bouche_ini():
    angle = 45
    set_angle(angle)
    time.sleep(4)
    angle = 2
    set_angle(angle)
    
#bouche_ini()
