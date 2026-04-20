from machine import Pin, I2C
import time
import _thread

angle_z = 0.0
last_time = time.ticks_ms()

gyro_ok = False
imu = None

try:
    from mpu6500 import MPU6500

    i2c = I2C(0, scl=Pin(22), sda=Pin(21))
    imu = MPU6500(i2c)

    gyro_ok = True
    print("Gyro détecté")

except OSError:
    print("Pas de gyro")


def update():
    global angle_z, last_time

    if not gyro_ok or imu is None:
        return   # 🔥 protection totale

    now = time.ticks_ms()
    dt = time.ticks_diff(now, last_time) / 1000.0
    last_time = now

    try:
        _, _, gz = imu.gyro
        angle_z += gz * 57.2958 * dt
    except:
        pass


def get_accel_z():
    if not gyro_ok or imu is None:
        return 0.0
    try:
        _, _, az = imu.acceleration
        return az - 10
    except:
        return 0.0


def get_angle():
    return angle_z if gyro_ok else 0.0

def _gyro_loop():
    while gyro_ok:
        update()
        time.sleep_ms(10)

def reset_angle():
    global angle_z, last_time
    angle_z = 0.0
    last_time = time.ticks_ms()
    

if gyro_ok:
    _thread.start_new_thread(_gyro_loop, ())

"""
from gyro import reset_angle, get_angle, get_accel_z
reset_angle()

while True:
    #z = get_angle()
    #print("Angle Z: {:.2f}".format(z))
    az = []
    for i in range(0, 20):
        az.append(get_accel_z())
        sleep(0.05)
    print(max(az))
    print(az)
"""
