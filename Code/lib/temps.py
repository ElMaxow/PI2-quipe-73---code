import time

_start = time.ticks_ms()

def reset_time():
    _start = time.ticks_ms()

def temps():
    return time.ticks_diff(time.ticks_ms(), _start) / 1000