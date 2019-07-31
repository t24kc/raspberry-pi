# chapter01
Let's activate the each sensors.

# Run
## CO2 Sensor
```zsh
$ python3 CCS811.py --help
usage: CCS811.py [-h] [-i INTERVAL]

CO2 Sensor Script

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds

$ python3 CCS811.py -i 5
```

## Infrared Distance Sensor
```zsh
$ python3 VL6180.py --help
usage: VL6180.py [-h] [-i INTERVAL]

Infrared Distance Sensor Script

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds

$ python3 VL6180.py -i 5
```

## Digital Light Sensor
```zsh
$ python3 BH1750FVI.py --help
usage: BH1750FVI.py [-h] [-i INTERVAL]

Digital Light Sensor Script

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds

$ python3 BH1750FVI.py -i 5
```

## Temperature and Humidity Sensor
```zsh
$ python3 SHT31.py --help
usage: SHT31.py [-h] [-i INTERVAL]

Temperature and Humidity Sensor Script

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds

$ python3 SHT31.py -i 5
```
