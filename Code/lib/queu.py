from machine import Pin, PWM
import time

servo = PWM(Pin(19), freq=50)  # servo sur GPIO 18

# servos 19 arriere et 13 avant

def set_angle(angle):
    duty = int(26 + (angle/180)*102)  # conversion angle -> PWM
    servo.duty(duty)

def queue():
    for i in range(3):
        set_angle(float(135+20))
        time.sleep(1)
        set_angle(float(45-10))
        time.sleep(1)
    set_angle(float(135+20))

def queue_ini():
    set_angle(float(135+20))

#queue()
    
#queue_ini()