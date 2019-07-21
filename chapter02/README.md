# chapter02
Let's start the relay module (switch function).

# Run
## Relay Module
```zsh
$ python3 relay_module.py --help
usage: relay_module.py [-h] [-c CHANNEL] [-w WAIT_TIME] [-i INTERVAL]

Relay Module Script

optional arguments:
  -h, --help            show this help message and exit
  -c CHANNEL, --channel CHANNEL
                        set channel (default 7 channel)
  -w WAIT_TIME, --wait-time WAIT_TIME
                        set power on wait seconds (default 3 seconds)
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds (default 10 seconds)

$ python3 relay_module.py -w 5 -i 5
```