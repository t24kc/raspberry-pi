from datetime import datetime
from lib.spread_sheet import SpreadSheet
from sensor.BH1750FVI import BH1750FVI
from sensor.CCS811 import CCS811
from sensor.SHT31 import SHT31
from sensor.VL6180 import VL6180X
from sensor.MCP300X import MCP300X

import argparse
import schedule

DEFAULT_KEY_PATH = "../.gcp/key.json"
DEFAULT_SHEET_ID = "dummy"
DEFAULT_COLUMNS = ["Time", "CO2", "TVOC", "Distance", "Light", "Temperature", "Humidity", "Wet"]
DEFAULT_INTERVAL_TIME = 600
DEFAULT_WET_LOWER_LIMIT = 450
DEFAULT_WATER_TURN_ON_TIME = 30


class Scheduler(object):
    def __init__(self, spread_sheet, wet_lower_limit, water_turn_on_time):
        self._spread_sheet = spread_sheet

        self._ccs811_sensor = CCS811()
        self._vl6180x_sensor = VL6180X()
        self._bh1750fvi_sensor = BH1750FVI()
        self._sht31_sensor = SHT31()
        self._mcp300x = MCP300X()

        self._wet_lower_limit = wet_lower_limit
        self._water_turn_on_time = water_turn_on_time

    def logging_job(self):
        current_datetime = datetime.now()
        self._ccs811_sensor.read_data()
        co2 = self._ccs811_sensor.get_eco2()
        tvoc = self._ccs811_sensor.get_tvoc()
        distance = self._vl6180x_sensor.get_distance()
        light = self._bh1750fvi_sensor.get_light()
        temperature, humidity = self._sht31_sensor.get_temperature_humidity()
        wet_level = self._mcp300x.get_wet_level()

        values = [current_datetime, co2, tvoc, distance, light, temperature, humidity, wet_level]
        print(values)
        self._spread_sheet.append_row(values)

    def water_job(self):
        wet_level = self._mcp300x.get_wet_level()
        if wet_level < self._wet_lower_limit:
            self._mcp300x.turn_on_water(self._water_turn_on_time)


def main():
    parser = argparse.ArgumentParser(description="Google Spread Sheet Script")
    parser.add_argument(
        "-k",
        "--key-path",
        type=str,
        default=DEFAULT_KEY_PATH,
        help="set service account key path (default {})".format(DEFAULT_KEY_PATH),
    )
    parser.add_argument(
        "-s",
        "--spread-sheet-id",
        type=str,
        default=DEFAULT_SHEET_ID,
        help="set spread sheet id",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_TIME,
        help="set script interval seconds (default {} seconds)".format(
            DEFAULT_INTERVAL_TIME
        ),
    )
    parser.add_argument(
        "-w",
        "--wet-lower-limit",
        type=int,
        default=DEFAULT_WET_LOWER_LIMIT,
        help="set wet lower limit (default {} mm)".format(
            DEFAULT_WET_LOWER_LIMIT
        ),
    )
    parser.add_argument(
        "-t",
        "--water-turn-on-time",
        type=int,
        default=DEFAULT_WATER_TURN_ON_TIME,
        help="set water turn on time (default {} seconds)".format(
            DEFAULT_WATER_TURN_ON_TIME
        ),
    )
    args = parser.parse_args()

    spread_sheet = SpreadSheet(args.key_path, args.spread_sheet_id)
    spread_sheet.append_row(DEFAULT_COLUMNS)

    scheduler = Scheduler(spread_sheet, args.wet_lower_limit, args.water_turn_on_time)
    schedule.every(args.interval).seconds.do(scheduler.logging_job)
    schedule.every(args.interval).seconds.do(scheduler.water_job)


if __name__ == "__main__":
    main()
