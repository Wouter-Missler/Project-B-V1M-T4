from machine import Pin
from time import sleep
gp16 = Pin(16, Pin.OUT)

while True:
    data = int(input())
    gp16(data)
    sleep(0.1)
