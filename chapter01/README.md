# chapter01
Let's activate the each sensors.

# Run
## CO2 and TVOC Sensor
```zsh
# show help message
$ python CCS811.py --help 
usage: CCS811.py [-h] [-i INTERVAL]

CO2 and TVOC Sensor Script

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds

$ python CCS811.py -i 5
```

## Infrared Distance Sensor
```zsh
$ python VL6180.py -i 5
```

## Digital Light Sensor
```zsh
$ python BH1750FVI.py -i 5
```

## Temperature and Humidity Sensor
```zsh
$ python SHT31.py -i 5
```
