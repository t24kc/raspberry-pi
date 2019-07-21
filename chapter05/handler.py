from datetime import datetime
from time import sleep
from lib.spread_sheet import SpreadSheet
from sensor.SHT31 import SHT31
from sensor.BH1750FVI import BH1750FVI
from sensor.VL6180 import VL6180X
from sensor.MCP300X import MCP300X

import argparse
import schedule

DEFAULT_KEY_PATH = "key.json"
DEFAULT_SHEET_ID = "dummy"
DEFAULT_COLUMNS = ["Time", "Distance", "Light", "Temperature", "Humidity", "WaterFlag"]
DEFAULT_INTERVAL_TIME = 600
DEFAULT_DISTANCE_LIMIT = 50
DEFAULT_WATER_TURN_ON_TIME = 30


class Scheduler(object):
    def __init__(self, spread_sheet, distance_limit, water_turn_on_time):
        self._spread_sheet = spread_sheet

        self._vl6180x_sensor = VL6180X()
        self._bh1750fvi_sensor = BH1750FVI()
        self._sht31_sensor = SHT31()
        self._mcp300x = MCP300X()

        self._distance_limit = distance_limit
        self._water_turn_on_time = water_turn_on_time

    def logging_job(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        distance = self._vl6180x_sensor.get_distance()
        light = self._bh1750fvi_sensor.get_light()
        temperature, humidity = self._sht31_sensor.get_temperature_humidity()
        water_flag = 1 if self.is_water_flag(distance) else 0

        values = [
            current_datetime,
            round(distance, 1),
            round(light, 1),
            round(temperature, 1),
            round(humidity, 1),
            water_flag
        ]
        print(values)
        self._spread_sheet.append_row(values)

    def water_job(self):
        distance = self._vl6180x_sensor.get_distance()
        if self.is_water_flag(distance):
            self._mcp300x.turn_on_water(self._water_turn_on_time)

    def is_water_flag(self, distance):
        return distance > self._distance_limit

    def turn_off_water(self):
        self._mcp300x.turn_off_water()


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
        "-d",
        "--distance-limit",
        type=int,
        default=DEFAULT_DISTANCE_LIMIT,
        help="set distance limit (default {} mm)".format(
            DEFAULT_DISTANCE_LIMIT
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

    scheduler = Scheduler(spread_sheet, args.distance_limit, args.water_turn_on_time)
    schedule.every(args.interval).seconds.do(scheduler.logging_job)
    schedule.every(args.interval).seconds.do(scheduler.water_job)

    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        scheduler.turn_off_water()
        pass


if __name__ == "__main__":
    main()
