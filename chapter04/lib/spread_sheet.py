from oauth2client.service_account import ServiceAccountCredentials
import gspread

SCOPE = [
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
            self._key_path, SCOPE)
        return gspread.authorize(credentials).open_by_key(self._spread_sheet_id)

    def get_label_value(self, label, index=DEFAULT_SHEET_INDEX):
        return self._get_client().get_worksheet(index).acell(label).value

    def set_label_value(self, label, value, index=DEFAULT_SHEET_INDEX):
        self._get_client().get_worksheet(index).update_acell(label, value)

    def append_row(self, values, index=DEFAULT_SHEET_INDEX):
        try:
            self._get_client().get_worksheet(index).append_row(values)
        except:
            pass
