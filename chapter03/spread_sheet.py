from oauth2client.service_account import ServiceAccountCredentials
import argparse
import gspread

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

DEFAULT_KEY_PATH = "key.json"
DEFAULT_SHEET_ID = "dummy"
DEFAULT_SHEET_INDEX = 0


class SpreadSheet(object):
    def __init__(self, key_path, spread_sheet_id):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_path, SCOPE)

        self.sheet_client = gspread.authorize(credentials).open_by_key(spread_sheet_id)

    def get_label_value(self, label, index=DEFAULT_SHEET_INDEX):
        return self.sheet_client.get_worksheet(index).acell(label).value

    def set_label_value(self, label, value, index=DEFAULT_SHEET_INDEX):
        self.sheet_client.get_worksheet(index).update_acell(label, value)


def main():
    default_input_text = 100
    default_label = "A1"

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
        "-l",
        "--label",
        type=str,
        default=default_label,
        help="set spread sheet cell label (default {})".format(default_label),
    )
    parser.add_argument(
        "-t",
        "--input-text",
        type=int,
        default=default_input_text,
        help="set script interval seconds (default {})".format(
            default_input_text
        ),
    )
    args = parser.parse_args()

    spread_sheet = SpreadSheet(args.key_path, args.spread_sheet_id)
    spread_sheet.set_label_value(args.label, args.input_text)


if __name__ == "__main__":
    main()
