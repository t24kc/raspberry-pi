# Soil Moisture Sensor
from logging import getLogger
from time import sleep
import spidev
import RPi.GPIO as GPIO

DEFAULT_CHANNEL = 7


class MCP300X(object):
    def __init__(self, channel=DEFAULT_CHANNEL):
        self._logger = getLogger(self.__class__.__name__)
        self._spi = spidev.SpiDev()
        self._channel = channel
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        self._logger.debug("MCP300X sensor is starting...")

    def get_wet_level(self):
        self._spi.open(0, 0)
        data = self._spi.xfer2([0x68, 0x00])
        wet_level = (data[0] * 256 + data[1]) & 0x3FF
        self._spi.close()

        return wet_level

    def turn_on_water(self, turn_on_time):
        print("turn on relay module {} seconds".format(turn_on_time))

        GPIO.setup(self._channel, GPIO.OUT)
        GPIO.output(self._channel, 0)
        sleep(turn_on_time)
        self.turn_off_water()

    def turn_off_water(self):
        GPIO.output(self._channel, 1)
