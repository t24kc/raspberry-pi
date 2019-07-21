# CO2 and TVOC Sensor
from collections import OrderedDict
from logging import getLogger
from time import sleep
import argparse
import smbus

ADDRESS = 0x5A

COMMAND_STATUS = 0x00
COMMAND_MEAS_MODE = 0x01
COMMAND_ALG_RESULT_DATA = 0x02
COMMAND_HW_ID = 0x20
COMMAND_BOOTLOADER_APP_START = 0xF4

HW_ID_CODE = 0x81

DRIVE_MODE_IDLE = 0x00
DRIVE_MODE_1SEC = 0x01
DRIVE_MODE_10SEC = 0x02
DRIVE_MODE_60SEC = 0x03
DRIVE_MODE_250MS = 0x04


class CCS811(object):
    def __init__(self, mode=DRIVE_MODE_1SEC, address=ADDRESS):
        self._logger = getLogger(self.__class__.__name__)

        if mode not in [
            DRIVE_MODE_IDLE,
            DRIVE_MODE_1SEC,
            DRIVE_MODE_10SEC,
            DRIVE_MODE_60SEC,
            DRIVE_MODE_250MS,
        ]:
            raise ValueError(
                "Unexpected mode value {0}.  Set mode to one of CCS811_DRIVE_MODE_IDLE, CCS811_DRIVE_MODE_1SEC, "
                "CCS811_DRIVE_MODE_10SEC, CCS811_DRIVE_MODE_60SEC or CCS811_DRIVE_MODE_250MS".format(
                    mode
                )
            )

        self._address = address
        self._bus = smbus.SMBus(1)

        self._status = Bitfield(
            [
                ("ERROR", 1),
                ("unused", 2),
                ("DATA_READY", 1),
                ("APP_VALID", 1),
                ("unused2", 2),
                ("FW_MODE", 1),
            ]
        )

        self._meas_mode = Bitfield(
            [("unused", 2), ("INT_THRESH", 1),
             ("INT_DATARDY", 1), ("DRIVE_MODE", 3)]
        )

        self._error_id = Bitfield(
            [
                ("WRITE_REG_INVALID", 1),
                ("READ_REG_INVALID", 1),
                ("MEASMODE_INVALID", 1),
                ("MAX_RESISTANCE", 1),
                ("HEATER_FAULT", 1),
                ("HEATER_SUPPLY", 1),
            ]
        )

        self._TVOC = 0
        self._eCO2 = 0

        if self.read(COMMAND_HW_ID) != HW_ID_CODE:
            raise Exception(
                "Device ID returned is not correct! Please check your wiring."
            )

        self.write_list(COMMAND_BOOTLOADER_APP_START, [])
        sleep(0.1)

        if self.check_error():
            raise Exception(
                "Device returned an Error! Try removing and reapplying power to the device and running the code again."
            )
        if not self._status.FW_MODE:
            raise Exception(
                "Device did not enter application mode! If you got here, "
                "there may be a problem with the firmware on your sensor."
            )

        self.disable_interrupt()
        self.set_drive_mode(mode)

        self._logger.debug("CCS811 sensor is starting...")

    def disable_interrupt(self):
        self._meas_mode.INT_DATARDY = 1
        self.write(COMMAND_MEAS_MODE, self._meas_mode.get())

    def set_drive_mode(self, mode):
        self._meas_mode.DRIVE_MODE = mode
        self.write(COMMAND_MEAS_MODE, self._meas_mode.get())

    def available(self):
        self._status.set(self.read(COMMAND_STATUS))
        if not self._status.DATA_READY:
            return False
        else:
            return True

    def read_data(self):
        if not self.available():
            return False
        else:
            buf = self.read_list(COMMAND_ALG_RESULT_DATA, 8)
            self._eCO2 = (buf[0] << 8) | (buf[1])
            self._TVOC = (buf[2] << 8) | (buf[3])
            if self._status.ERROR:
                return buf[5]
            else:
                return 0

    def get_tvoc(self):
        """Get TVOC data from sensor and return it."""
        return self._TVOC

    def get_eco2(self):
        """Get eCO2 data from sensor and return it."""
        return self._eCO2

    def check_error(self):
        self._status.set(self.read(COMMAND_STATUS))
        return self._status.ERROR

    def read(self, register):
        return self._bus.read_byte_data(self._address, register) & 0xFF

    def write(self, register, value):
        value = value & 0xFF
        self._bus.write_byte_data(self._address, register, value)

    def read_list(self, register, length):
        return self._bus.read_i2c_block_data(self._address, register, length)

    def write_list(self, register, data):
        self._bus.write_i2c_block_data(self._address, register, data)


class Bitfield(object):
    def __init__(self, _structure):
        self._structure = OrderedDict(_structure)
        for key, value in self._structure.items():
            setattr(self, key, 0)

    def get(self):
        fullreg = 0
        pos = 0
        for key, value in self._structure.items():
            fullreg = fullreg | (
                (getattr(self, key) & (2 ** value - 1)) << pos)
            pos = pos + value

        return fullreg

    def set(self, data):
        pos = 0
        for key, value in self._structure.items():
            setattr(self, key, (data >> pos) & (2 ** value - 1))
            pos = pos + value


def main():
    parser = argparse.ArgumentParser(description="CO2 and TVOC Sensor Script")
    parser.add_argument(
        "-i", "--interval", type=int, default=10, help="set script interval seconds"
    )
    args = parser.parse_args()

    sensor = CCS811()
    while True:
        if not sensor.read_data():
            print("CO2: {} ppm, TVOC: {}".format(
                sensor.get_eco2(), sensor.get_tvoc()))
        else:
            print("Error!")
        sleep(args.interval)


if __name__ == "__main__":
    main()
