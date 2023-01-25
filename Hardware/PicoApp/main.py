from machine import Pin
from time import sleep
import RGB1602

gp16 = Pin(16, Pin.OUT)
lcd = RGB1602.RGB1602(16, 2)


def fade(lcd, fade_in=True):
    for i in range(256):
        v = i if fade_in else 255 - i
        lcd.set_rgb(v, v, v)
        sleep(0.01)

# bij opstarten
lcd.clear()
fade(lcd, fade_in=True)

while True:
    data = input()
    lcd.clear()
    #lcd.printout("Vrienden online")
    #data = input()
    lcd.printout(data)
    sleep(0.1)
