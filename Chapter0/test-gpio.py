import time
from gpiozero import LED
led = LED(4)
led.on()
time.sleep(10)
