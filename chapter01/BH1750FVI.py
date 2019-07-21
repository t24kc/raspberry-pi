# Digital Light Sensor
from logging import getLogger
from time import sleep
import argparse
import smbus

ADDRESS = 0x23

COMMAND_POWER_DOWN = 0x00
COMMAND_POWER_ON = 0x01
COMMAND_RESET = 0x07

# Start measurement at 4lx resolution. Time typically 16ms.
COMMAND_CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
COMMAND_CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
COMMAND_CONTINUOUS_HIGH_RES_MODE_2 = 0x11

# Device is automatically set to Power Down after measurement.
# Start measurement at 1lx resolution. Time typically 120ms
COMMAND_ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
COMMAND_ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
COMMAND_ONE_TIME_LOW_RES_MODE = 0x23


class BH1750FVI(object):
    def __init__(self, address=ADDRESS):
        self._logger = getLogger(self.__class__.__name__)
        self._address = address
        self._bus = smbus.SMBus(1)

        self._logger.debug("BH1750 sensor is starting...")

    def _set_mode(self, mode):
        self.write(mode)

    def power_down(self):
        self._set_mode(COMMAND_POWER_DOWN)

    def power_on(self):
        self._set_mode(COMMAND_POWER_ON)

    def reset(self):
        self.power_on()
        self._set_mode(COMMAND_RESET)

    def get_light(self, command=COMMAND_ONE_TIME_HIGH_RES_MODE_1):
        """Read the lux (light value) from the sensor and return it."""
        light = self.read(command)
        return self.convert_to_number(light)

    def read(self, register):
        return self._bus.read_i2c_block_data(self._address, register)

    def write(self, register):
        self._bus.write_byte(self._address, register)

    @staticmethod
    def convert_to_number(data):
        # Simple function to convert 2 bytes of data into a decimal number.
        return (data[1] + (256 * data[0])) / 1.2


def main():
    parser = argparse.ArgumentParser(description="Digital Light Sensor Script")
    parser.add_argument("-i", "--interval", type=int, default=10, help="set script interval seconds")
    args = parser.parse_args()

    sensor = BH1750FVI()
    while True:
        print("Light Level (1x gain): {} lux".format(sensor.get_light()))
        sleep(args.interval)


if __name__ == "__main__":
    main()
