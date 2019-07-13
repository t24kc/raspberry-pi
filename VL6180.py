#!/usr/bin/python
import time
import smbus

addr = 0x29
bus = smbus.SMBus(1)

VL6180X_SYSTEM_FRESH_OUT_OF_RESET = 0x0016
VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME = 0x001C
VL6180X_SYSRANGE_RANGE_CHECK_ENABLES = 0x002D
VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE = 0x0022
VL6180X_SYSALS_INTEGRATION_PERIOD = 0x0040
VL6180X_SYSALS_ANALOGUE_GAIN = 0x3F
VL6180X_FIRMWARE_RESULT_SCALER = 0x0120
VL6180X_SYSRANGE_START = 0x0018
VL6180X_RESULT_RANGE_VAL = 0x0062
VL6180X_SYSTEM_INTERRUPT_CLEAR = 0x0015
VL6180X_SYSALS_START = 0x0038
VL6180X_RESULT_ALS_VAL = 0x0050


def read(register16):
    a1 = (register16 >> 8) & 0xFF
    a0 = register16 & 0xFF
    bus.write_i2c_block_data(addr, a1, [a0])
    return bus.read_byte(addr)


def read16(register16):
    a1 = (register16 >> 8) & 0xFF
    a0 = register16 & 0xFF

    bus.write_i2c_block_data(addr, a1, [a0])
    data16h = bus.read_byte(addr)
    data16l = bus.read_byte(addr)
    return (data16h << 8) | (data16l & 0xFF)


def WriteByte(register16, data):
    a1 = (register16 >> 8) & 0xFF
    a0 = register16 & 0xFF
    bus.write_i2c_block_data(addr, a1, [a0, (data & 0xFF)])


def WriteByte16(register16, data16):
    a1 = (register16 >> 8) & 0xFF
    a0 = register16 & 0xFF
    d1 = (data16 >> 8) & 0xFF
    d0 = data16 & 0xFF
    bus.write_i2c_block_data(addr, a1, [a0, d1, d0])


# init
if read(VL6180X_SYSTEM_FRESH_OUT_OF_RESET) == 1:
    print("sensor is ready.")
    WriteByte(0x0207, 0x01)
    WriteByte(0x0208, 0x01)
    WriteByte(0x0096, 0x00)
    WriteByte(0x0097, 0xFD)
    WriteByte(0x00E3, 0x00)
    WriteByte(0x00E4, 0x04)
    WriteByte(0x00E5, 0x02)
    WriteByte(0x00E6, 0x01)
    WriteByte(0x00E7, 0x03)
    WriteByte(0x00F5, 0x02)
    WriteByte(0x00D9, 0x05)
    WriteByte(0x00DB, 0xCE)

    WriteByte(0x00DC, 0x03)
    WriteByte(0x00DD, 0xF8)
    WriteByte(0x009F, 0x00)
    WriteByte(0x00A3, 0x3C)
    WriteByte(0x00B7, 0x00)
    WriteByte(0x00BB, 0x3C)
    WriteByte(0x00B2, 0x09)
    WriteByte(0x00CA, 0x09)
    WriteByte(0x0198, 0x01)
    WriteByte(0x01B0, 0x17)
    WriteByte(0x01AD, 0x00)
    WriteByte(0x00FF, 0x05)
    WriteByte(0x0100, 0x05)
    WriteByte(0x0199, 0x05)
    WriteByte(0x01A6, 0x1B)
    WriteByte(0x01AC, 0x3E)
    WriteByte(0x01A7, 0x1F)
    WriteByte(0x0030, 0x00)

# default_settings
# Recommended : Public registers - See data sheet for more detail
WriteByte(0x0011, 0x10)
# Enables polling for 'New Sample ready' when measurement completes
WriteByte(0x010A, 0x30)
# Set the averaging sample period (compromise between lower noise and increased execution time)
WriteByte(0x003F, 0x46)
# Sets the light and dark gain (upper nibble). Dark gain should not be changed.
WriteByte(0x0031, 0xFF)
# sets the # of range measurements after which auto calibration of system is performed
WriteByte(0x0040, 0x63)
# Set ALS integration time to 100ms DocID026571 Rev 1 25/27 AN4545 SR03 settings27
WriteByte(0x002E, 0x01)
# perform a single temperature calibration of the ranging sensor

# Optional: Public registers - See data sheet for more detail
WriteByte(0x001B, 0x09)
# Set default ranging inter-measurement period to 100ms
WriteByte(0x003E, 0x31)
# Set default ALS inter-measurement period to 500ms
WriteByte(0x0014, 0x24)
# Configures interrupt on 'New Sample Ready threshold event'
WriteByte(0x016, 0x00)
# change fresh out of set status to 0

# Additional settings defaults from community
WriteByte(VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME, 0x32)
WriteByte(VL6180X_SYSRANGE_RANGE_CHECK_ENABLES, 0x10 | 0x01)
WriteByte16(VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE, 0x7B)
WriteByte16(VL6180X_SYSALS_INTEGRATION_PERIOD, 0x64)  # 100ms
WriteByte(VL6180X_SYSALS_ANALOGUE_GAIN, 0x20)  # x40
WriteByte(VL6180X_FIRMWARE_RESULT_SCALER, 0x01)

# main
# distance
WriteByte(VL6180X_SYSRANGE_START, 0x01)  # 0x03 renzoku
time.sleep(0.1)
distance = read(VL6180X_RESULT_RANGE_VAL)
WriteByte(VL6180X_SYSTEM_INTERRUPT_CLEAR, 0x07)
print(distance, "mm")

# ambient_light
WriteByte(VL6180X_SYSALS_START, 0x01)
time.sleep(0.5)
light = read16(VL6180X_RESULT_ALS_VAL)
WriteByte(VL6180X_SYSTEM_INTERRUPT_CLEAR, 0x07)
# print read(VL6180X_SYSALS_ANALOGUE_GAIN)
# print read16(VL6180X_SYSALS_INTEGRATION_PERIOD)
print(light * 0.32 * 100 / (32 * 100), "lux")
# Copyright (c) 2014-2015 Arnie Weber. All rights reserved.
