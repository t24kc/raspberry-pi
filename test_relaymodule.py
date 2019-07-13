import RPi.GPIO as GPIO
import time
import sys

if len(sys.argv) < 2:
    print("notime")
    quit()

try:
    pump_time = int(sys.argv[1])
except Exception:
    print("bad time")
    quit()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7,False)
time.sleep(pump_time)
GPIO.output(7,GPIO.OUT)
GPIO.cleanup()


