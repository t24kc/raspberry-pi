from datetime import datetime
from time import sleep
from lib.spread_sheet import SpreadSheet
from lib.mail import Mail
from sensor.SHT31 import SHT31
from sensor.BH1750FVI import BH1750FVI
from sensor.VL6180 import VL6180X
from sensor.MCP300X import MCP300X
from sensor.CCS811 import CCS811

import schedule
import yaml

DEFAULT_COLUMNS = [
    "Time", "Distance(mm)", "Light(lux)", "Light(klux/h)",
    "Temperature(C)", "Humidity(%)", "CO2(ppm)", "WaterFlag"
]


class Scheduler(object):
    def __init__(self, config):
        self.params = {
            "distance": None,
            "light": None,
            "light_klux": None,
            "light_total": 0,
            "temperature": None,
            "humidity": None,
            "co2": None,
            "alert_remaining": config["alert"]["consecutive_time"],
        }

        self._config = config

        self._spread_sheet_client = SpreadSheet(
            self._config["google"]["key_path"],
            self._config["google"]["spread_sheet_id"],
        )
        if not self._spread_sheet_client.get_label_value("A1"):
            self._spread_sheet_client.append_row(DEFAULT_COLUMNS)

        self._mail_client = Mail(self._config["google"]["key_path"])

        self._vl6180x_sensor = VL6180X()
        self._bh1750fvi_sensor = BH1750FVI()
        self._sht31_sensor = SHT31()
        self._mcp300x = MCP300X()
        self._ccs811_sensor = CCS811()

    def monitoring_job(self):
        self._fetch_params()
        self._logging_params()
        self._alert_params()
        if self._is_water_flag():
            self.turn_on_water()

    def mail_job(self):
        pass

    def _fetch_params(self):
        light = self._bh1750fvi_sensor.get_light()
        light_klux = light * self._config["scheduler"]["monitoring_interval_minutes"] / 60000

        self._ccs811_sensor.read_data()
        self.params.update({
            "distance": self._vl6180x_sensor.get_distance(),
            "light": light,
            "light_klux": light_klux,
            "temperature": self._sht31_sensor.get_temperature(),
            "humidity": self._sht31_sensor.get_humidity(),
            "co2": self._ccs811_sensor.get_co2(),
        })
        self.params["light_total"] += light_klux

    def _logging_params(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        values = [
            current_datetime,
            round(self.params["distance"], 1),
            round(self.params["light"], 1),
            round(self.params["light_klux"], 1),
            round(self.params["temperature"], 1),
            round(self.params["humidity"], 1),
            round(self.params["co2"], 1),
            int(self._is_water_flag())
        ]
        print(values)
        self._spread_sheet_client.append_row(values)

    def _alert_params(self):
        if self.params["temperature"] < self._config["alert"]["temperature_lower_limit"] \
                or self._config["alert"]["temperature_upper_limit"] < self.params["temperature"] \
                or self.params["co2"] < self._config["alert"]["co2_lower_limit"] \
                or self._config["alert"]["co2_upper_limit"] < self.params["co2"]:
            self.params["alert_remaining"] -= 1

        if self.params["alert_remaining"] <= 0:
            pass

    def _is_water_flag(self):
        return self.params["light_total"] > self._config["sensor"]["solar_radiation_limit"]

    def turn_on_water(self):
        self.params["light_total"] = 0
        self._mcp300x.turn_on_water(self._config["sensor"]["water_turn_on_time"])

    def turn_off_water(self):
        self._mcp300x.turn_off_water()


def main():
    with open("config.yaml") as file:
        config = yaml.full_load(file)

    scheduler = Scheduler(config)
    schedule.every(config["scheduler"]["monitoring_interval_minutes"]).minutes.do(scheduler.monitoring_job)
    schedule.every(config["scheduler"]["summary_mail_interval_days"]).days.do(scheduler.mail_job)

    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        scheduler.turn_off_water()
        pass


if __name__ == "__main__":
    main()
