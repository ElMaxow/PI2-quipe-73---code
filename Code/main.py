from principal import lets_go
from gyro import get_accel_z
from temps import temps
from time import sleep
from machine import Pin
from placer_jouet import bouche_ini
from avancer_wifi import wifi_start

print("slaut")
# Mettre ici en vrai si tu veux bypass le gyro
condition = False

led_b = Pin(2, Pin.OUT)
bouton = Pin(32, Pin.IN, Pin.PULL_UP)  # bouton sur GPIO 12

alpha = True
accel = False
c = 0
e = 0
f = False # pour ne pas ouvrir la bouche au depart

while alpha and temps() < 100 :
    print(c)
    if bouton.value() == 0:
        e += 1
        f = True
        if e == 35:
            print("lets go wifi")
            wifi_start()
            alpha = False
    #if c == 0:
        #print("waf waf")
        #bouche_ini()
    #a = get_accel_z()
    #print(a)
    #if abs(a) >= 3:
        #accel = True
    if (c+1) % 30 == 0 and e == 0 or condition:
        alpha = False
        #sleep(3)
        print("bouche =", f, "e=", e)
        lets_go(bouche_deb = f)
        
    if (c+1) % 100 == 0 or condition and e > 0:
        alpha = False
        #sleep(3)
        print("bouche =", f)
        lets_go(bouche_deb = f)
    if c % 5 == 0:
        led_b.value(not led_b.value())
    sleep(0.1)
    c += 1
    

led_b.off()
print("stop")