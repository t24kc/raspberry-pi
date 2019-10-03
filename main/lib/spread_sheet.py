from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

import gspread
import pandas as pd

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

DEFAULT_SHEET_INDEX = 0


class SpreadSheet(object):
    def __init__(self, key_path, spread_sheet_id):
        self._key_path = key_path
        self._spread_sheet_id = spread_sheet_id

    def _get_client(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._key_path, SCOPES)
        return gspread.authorize(credentials).open_by_key(self._spread_sheet_id)

    def get_label_value(self, label, index=DEFAULT_SHEET_INDEX):
        return self._get_client().get_worksheet(index).acell(label).value

    def set_label_value(self, label, value, index=DEFAULT_SHEET_INDEX):
        self._get_client().get_worksheet(index).update_acell(label, value)

    def col_values(self, col, index=DEFAULT_SHEET_INDEX):
        try:
            return self._get_client().get_worksheet(index).col_values(col)
        except Exception as e:
            print(e)
            pass

    def get_all_values(self, index=DEFAULT_SHEET_INDEX):
        try:
            return self._get_client().get_worksheet(index).get_all_values()
        except Exception as e:
            print(e)
            pass

    def append_row(self, values, index=DEFAULT_SHEET_INDEX):
        try:
            self._get_client().get_worksheet(index).append_row(values)
        except Exception as e:
            print(e)
            pass

    def get_dataframe(self, diff_days, index=DEFAULT_SHEET_INDEX):
        dframe = pd.DataFrame(self.get_all_values(index))
        dframe.columns = list(dframe.iloc[0])
        dframe.drop(0, axis=0, inplace=True)
        dframe = dframe.astype({
            "Time": "datetime64[ns]", "Distance(mm)": float, "Light(lux)": float,
            "Light(klux/h)": float, "Temperature(C)": float, "Humidity(%)": float,
            "CO2(ppm)": float, "WaterFlag": int
        })

        target_date = (datetime.now() - timedelta(days=diff_days)).strftime("%Y-%m-%d %H:%M:%S")
        return dframe.query("Time > '{}'".format(target_date)).reset_index(drop=True)
