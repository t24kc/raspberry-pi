from datetime import datetime
from time import sleep
from lib.spread_sheet import SpreadSheet
from sensor.SHT31 import SHT31
from sensor.BH1750FVI import BH1750FVI
from sensor.VL6180 import VL6180X

import argparse
import schedule

DEFAULT_KEY_PATH = "key.json"
DEFAULT_SHEET_ID = "dummy"
DEFAULT_COLUMNS = ["Time", "Distance", "Light", "Temperature", "Humidity"]
DEFAULT_INTERVAL_TIME = 600


class Scheduler(object):
    def __init__(self, spread_sheet):
        self._spread_sheet = spread_sheet
        self._vl6180x_sensor = VL6180X()
        self._bh1750fvi_sensor = BH1750FVI()
        self._sht31_sensor = SHT31()

    def job(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        distance = self._vl6180x_sensor.get_distance()
        light = self._bh1750fvi_sensor.get_light()
        temperature, humidity = self._sht31_sensor.get_temperature_humidity()

        values = [current_datetime, round(distance, 1), round(light, 1), round(temperature, 1), round(humidity, 1)]
        print(values)
        self._spread_sheet.append_row(values)


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
    args = parser.parse_args()

    spread_sheet = SpreadSheet(args.key_path, args.spread_sheet_id)
    spread_sheet.append_row(DEFAULT_COLUMNS)

    scheduler = Scheduler(spread_sheet)
    schedule.every(args.interval).seconds.do(scheduler.job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
