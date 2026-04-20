from machine import Pin, PWM
import time

servo = PWM(Pin(13), freq=50)  # servo sur GPIO 18

def set_angle(angle):
    duty = int(26 + (angle/180)*102)  # conversion angle -> PWM
    servo.duty(duty)

def placer_jouet():
    angle = 45
    set_angle(float(angle))
    time.sleep(2)
    angle = 2
    set_angle(float(angle))
    time.sleep(1)
