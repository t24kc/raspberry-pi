# Temperature and Humidity Sensor
from logging import getLogger
from time import sleep
import argparse
import smbus

ADDRESS = 0x44

COMMAND_MEAS_HIGHREP = 0x2C
COMMAND_RESULT = 0x00


class SHT31(object):
    def __init__(self, address=ADDRESS):
        self._logger = getLogger(self.__class__.__name__)
        self._address = address
        self._bus = smbus.SMBus(1)

        self._logger.debug("SHT31 sensor is starting...")

    def get_temperature(self):
        """Read the temperature from the sensor and return it."""
        temperature, humidity = self.get_temperature_humidity()
        return temperature

    def get_humidity(self):
        """Read the humidity from the sensor and return it."""
        temperature, humidity = self.get_temperature_humidity()
        return humidity

    def get_temperature_humidity(self):
        self.write_list(COMMAND_MEAS_HIGHREP, [0x06])
        sleep(0.5)

        data = self.read_list(COMMAND_RESULT, 6)
        temperature = -45 + (175 * (data[0] * 256 + data[1]) / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        return temperature, humidity

    def read(self, register):
        return self._bus.read_byte_data(self._address, register) & 0xFF

    def read_list(self, register, length):
        return self._bus.read_i2c_block_data(
            self._address, register, length)

    def write(self, register, value):
        value = value & 0xFF
        self._bus.write_byte_data(self._address, register, value)

    def write_list(self, register, data):
        self._bus.write_i2c_block_data(self._address, register, data)


def main():
    parser = argparse.ArgumentParser(description="Temperature and Humidity Sensor Script")
    parser.add_argument("-i", "--interval", type=int, default=10, help="set script interval seconds")
    args = parser.parse_args()

    sensor = SHT31()
    while True:
        temperature, humidity = sensor.get_temperature_humidity()
        print("Temperature: {} C, Humidity: {} %".format(temperature, humidity))
        sleep(args.interval)


if __name__ == "__main__":
    main()
