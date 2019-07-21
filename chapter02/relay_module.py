from time import sleep
import RPi.GPIO as GPIO
import argparse

DEFAULT_CHANNEL = 7
DEFAULT_WAIT_TIME = 3
DEFAULT_INTERVAL_TIME = 10


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)


def power_on(channel, interval):
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, 0)
    sleep(interval)
    GPIO.output(channel, 1)
    GPIO.cleanup()


def main():
    parser = argparse.ArgumentParser(description="Relay Module Script")
    parser.add_argument(
        "-c",
        "--channel",
        type=int,
        default=DEFAULT_CHANNEL,
        help="set channel (default {} channel)".format(DEFAULT_CHANNEL),
    )
    parser.add_argument(
        "-w",
        "--wait-time",
        type=int,
        default=DEFAULT_WAIT_TIME,
        help="set power on wait seconds (default {} seconds)".format(
            DEFAULT_WAIT_TIME),
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_TIME,
        help="set script interval seconds (default {} seconds)".format(
            DEFAULT_INTERVAL_TIME
        ),
    )
    args = parser.parse_args()

    init()
    sleep(args.wait_time)
    power_on(args.channel, args.interval)


if __name__ == "__main__":
    main()
