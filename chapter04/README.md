# chapter04
Let's write the values of all sensors value to GoogleSpreadSheet.

# Run
## Write All Sensors to Google Spread Sheet
```zsh
$ python3 handler.py --help
usage: handler.py [-h] [-k KEY_PATH] [-s SPREAD_SHEET_ID] [-i INTERVAL]

Google Spread Sheet Script

optional arguments:
  -h, --help            show this help message and exit
  -k KEY_PATH, --key-path KEY_PATH
                        set service account key path (default key.json)
  -s SPREAD_SHEET_ID, --spread-sheet-id SPREAD_SHEET_ID
                        set spread sheet id
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds (default 600 seconds)

# update DEFAULT_SHEET_ID
$ python3 handler.py -i 60
```