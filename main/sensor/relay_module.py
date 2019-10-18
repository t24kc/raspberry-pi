# Relay Module
from logging import getLogger
from time import sleep
import spidev
import RPi.GPIO as GPIO

DEFAULT_CHANNEL = 7


class RelayModule(object):
    def __init__(self, channel=DEFAULT_CHANNEL):
        self._logger = getLogger(self.__class__.__name__)
        self._spi = spidev.SpiDev()
        self._channel = channel
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        self._logger.debug("relay module is starting...")

    def turn_on_water(self, turn_on_time):
        print("turn on relay module {} seconds".format(turn_on_time))

        GPIO.setup(self._channel, GPIO.OUT)
        GPIO.output(self._channel, 0)
        sleep(turn_on_time)
        self.turn_off_water()

    def turn_off_water(self):
        GPIO.output(self._channel, 1)
