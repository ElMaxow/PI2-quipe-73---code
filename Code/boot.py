from machine import ADC, Pin, deepsleep
from time import sleep

adc = ADC(Pin(33))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

Vref = 3.3
def read_adc_avg(n=10):
    total = 0
    for _ in range(n):
        total += adc.read()
    return total / n

raw = read_adc_avg()
voltage_adc = (raw / 4095) * Vref
voltage_cell = voltage_adc * 13

min_V = 6 + 0.5
max_V = 8.4
delat_V = max_V - min_V

print("Tension batterie {:.2f} V".format(voltage_cell), "| {:.0f}".format((delat_V-(max_V-voltage_cell))*100/delat_V), "%")
print("NE PAS UTILISER EN DESSOUS DE", "{:.2f}".format(min_V), "V")

# Vérification tension
if 3 <= voltage_cell <= 6:
    print("Tension critique ({:.2f} V) → mode veille".format(voltage_cell))
    sleep(1)       
    deepsleep()     