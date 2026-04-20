from machine import Pin
from time import sleep


def led(time=1):
    for i in range(3):
        LED = Pin(4, Pin.OUT)
        LED.on()
        sleep(time)
        LED.off()
        sleep(time)

#led()

"""
for i in range(10):
    print(i)
    sleep(0.1)
"""
