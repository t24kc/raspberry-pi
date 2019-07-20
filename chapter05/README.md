# chapter05
Let's carry out watering when the water depth falls below a certain value.

# Run
## Write All Sensors to Google Spread Sheet and Trun on water
```zsh
$ python handler.py --help
usage: handler.py [-h] [-k KEY_PATH] [-s SPREAD_SHEET_ID] [-i INTERVAL]
                  [-w WET_LOWER_LIMIT] [-t WATER_TURN_ON_TIME]

Google Spread Sheet Script

optional arguments:
  -h, --help            show this help message and exit
  -k KEY_PATH, --key-path KEY_PATH
                        set service account key path (default
                        ../.gcp/key.json)
  -s SPREAD_SHEET_ID, --spread-sheet-id SPREAD_SHEET_ID
                        set spread sheet id
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds (default 600 seconds)
  -w WET_LOWER_LIMIT, --wet-lower-limit WET_LOWER_LIMIT
                        set wet lower limit (default 450 mm)
  -t WATER_TURN_ON_TIME, --water-turn-on-time WATER_TURN_ON_TIME
                        set water turn on time (default 30 seconds)

# update DEFAULT_SHEET_ID
$ python handler.py -i 60 -w 100 -t 30
```