# https://qiita.com/kwt514/items/33483238b25aafd1dc6a
# irrigation.py

import spidev
import time
import datetime
import subprocess
import RPi.GPIO as GPIO

wet_low = 450
water_check_enable = True
water_wait_count = 0
check_reset = 10


def write_log(log_text):
    f = open("/var/log/water", "a")
    d = datetime.datetime.today()
    f.write(d.strftime("%Y-%m-%d %H:%M:%S" + "," + log_text + "\n"))
    # print log_text
    f.close()


def read_wet_level():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    resp = spi.xfer2([0x68, 0x00])
    value = (resp[0] * 256 + resp[1]) & 0x3FF
    write_log("wet_level:" + str(value))
    spi.close()
    return value


def water():
    write_log("***** water start *****")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, True)
    time.sleep(30)
    GPIO.output(16, False)
    GPIO.cleanup()

    write_log("***** water end *****")


while True:
    wet_level = read_wet_level()

    if not water_check_enable:
        water_wait_count += 1
        if water_wait_count > check_reset:
            water_check_enable = True
            water_wait_count = 0

    if wet_level < wet_low and water_check_enable:
        water_check_enable = False
        water()
    time.sleep(300)
