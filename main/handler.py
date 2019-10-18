from datetime import datetime
from time import sleep
from lib.mail import Mail
from lib.spread_sheet import SpreadSheet
from sensor.SHT31 import SHT31
from sensor.BH1750FVI import BH1750FVI
from sensor.VL6180 import VL6180X
from sensor.CO2MINI import CO2MINI
from sensor.relay_module import RelayModule

import matplotlib.pyplot as plt
import schedule
import yaml

DEFAULT_COLUMNS = [
    "Time",
    "Distance(mm)",
    "Light(lux)",
    "Light(klux/h)",
    "Temperature(C)",
    "Humidity(%)",
    "CO2(ppm)",
    "WaterFlag",
]
DEFAULT_DATA_IMAGE_PATH = "data/figure.png"


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
            "alert_remaining": None,
        }

        self._config = config
        self._full_alert_remaining()

        self._mail_client = Mail(
            self._config["google"]["credentials_path"],
            self._config["google"]["token_path"],
        )
        self._spread_sheet_client = SpreadSheet(
            self._config["google"]["service_account_path"],
            self._config["google"]["spread_sheet_id"],
        )
        if not self._spread_sheet_client.get_label_value("A1"):
            self._spread_sheet_client.append_row(DEFAULT_COLUMNS)

        self._vl6180x_sensor = VL6180X()
        self._bh1750fvi_sensor = BH1750FVI()
        self._sht31_sensor = SHT31()
        self._relay_module = RelayModule()
        self._co2mini_sensor = CO2MINI()

    def monitoring_job(self):
        self._fetch_params()
        self._logging_params()
        self._alert_params()
        if self._is_water_flag():
            self.turn_on_water()

    def mail_job(self):
        dframe = self._spread_sheet_client.get_dataframe(diff_days=7)

        kwargs = {"kind": "line", "use_index": True, "rot": 45}
        setting_list = [
            {"title": "Light(lux)", "x": "Time", "y": "Light(lux)"},
            {"title": "CO2(ppm)", "x": "Time", "y": "CO2(ppm)"},
            {"title": "Temperature(C)", "x": "Time", "y": "Temperature(C)"},
            {"title": "Humidity(%)", "x": "Time", "y": "Humidity(%)"},
        ]
        fig, axes = plt.subplots(
            ncols=2, nrows=2, figsize=(20, 15), sharex="col")
        for ax, setting in zip(axes.ravel(), setting_list):
            dframe.plot(
                setting["x"], setting["y"], ax=ax, **kwargs, title=setting["title"]
            )

        plt.savefig(DEFAULT_DATA_IMAGE_PATH)
        self._send_mail(
            self._config["mail"]["summary"]["subject"],
            self._config["mail"]["summary"]["body"],
            DEFAULT_DATA_IMAGE_PATH,
        )

    def _fetch_params(self):
        light = self._bh1750fvi_sensor.get_light()
        light_klux = (
            light *
            self._config["scheduler"]["monitoring_interval_minutes"] / 60000
        )

        self._co2mini_sensor.read_data()
        self.params.update(
            {
                "distance": self._vl6180x_sensor.get_distance(),
                "light": light,
                "light_klux": light_klux,
                "temperature": self._sht31_sensor.get_temperature(),
                "humidity": self._sht31_sensor.get_humidity(),
                "co2": self._co2mini_sensor.get_co2(),
            }
        )
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
            int(self._is_water_flag()),
        ]
        self._spread_sheet_client.append_row(values)
        print(values)

    def _alert_params(self):
        if not self._is_alert_flag():
            self._full_alert_remaining()
            return

        self.params["alert_remaining"] -= 1
        if self.params["alert_remaining"] > 0:
            return

        body = ""
        if self._is_temperature_upper_limit():
            body = self._config["mail"]["alert"]["body"]["temperature_upper"].format(
                self.params["temperature"]
            )
        elif self._is_temperature_lower_limit():
            body = self._config["mail"]["alert"]["body"]["temperature_lower"].format(
                self.params["temperature"]
            )
        elif self._is_co2_upper_limit():
            body = self._config["mail"]["alert"]["body"]["co2_upper"].format(
                self.params["co2"]
            )
        elif self._is_co2_lower_limit():
            body = self._config["mail"]["alert"]["body"]["co2_lower"].format(
                self.params["co2"]
            )
        self._send_mail(self._config["mail"]["alert"]["subject"], body)
        self._full_alert_remaining()

    def _send_mail(self, subject, body, image_file=None):
        if image_file:
            message = self._mail_client.create_message_with_image(
                self._config["mail"]["to_address"], subject, body, image_file
            )
        else:
            message = self._mail_client.create_message(
                self._config["mail"]["to_address"], subject, body
            )
        self._mail_client.send_message(message)

    def _full_alert_remaining(self):
        self.params["alert_remaining"] = self._config["alert"]["consecutive_time"]

    def _is_alert_flag(self):
        return (
            self._is_temperature_upper_limit()
            or self._is_temperature_lower_limit()
            or self._is_co2_upper_limit()
            or self._is_co2_lower_limit()
        )

    def _is_temperature_upper_limit(self):
        return (
            self._config["alert"]["temperature_upper_limit"]
            < self.params["temperature"]
        )

    def _is_temperature_lower_limit(self):
        return (
            self.params["temperature"]
            < self._config["alert"]["temperature_lower_limit"]
        )

    def _is_co2_upper_limit(self):
        return self._config["alert"]["co2_upper_limit"] < self.params["co2"]

    def _is_co2_lower_limit(self):
        return self.params["co2"] < self._config["alert"]["co2_lower_limit"]

    def _is_water_flag(self):
        return (
            self.params["light_total"] > self._config["sensor"]["solar_radiation_limit"]
        )

    def turn_on_water(self):
        self.params["light_total"] = 0
        self._relay_module.turn_on_water(
            self._config["sensor"]["water_turn_on_time"])

    def turn_off_water(self):
        self._relay_module.turn_off_water()


def main():
    with open("config.yaml") as file:
        config = yaml.full_load(file)

    scheduler = Scheduler(config)
    schedule.every(config["scheduler"]["monitoring_interval_minutes"]).minutes.do(
        scheduler.monitoring_job
    )
    schedule.every(config["scheduler"]["summary_mail_interval_days"]).days.do(
        scheduler.mail_job
    )

    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        scheduler.turn_off_water()
        pass


if __name__ == "__main__":
    main()
