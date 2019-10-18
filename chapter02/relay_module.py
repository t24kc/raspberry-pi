from time import sleep
import RPi.GPIO as GPIO
import argparse
import schedule

DEFAULT_CHANNEL = 7
DEFAULT_WAIT_TIME = 3
DEFAULT_INTERVAL_TIME = 10


class Scheduler(object):
    def __init__(self, channel):
        self._channel = channel
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    def power_on_and_off(self, interval):
        GPIO.setup(self._channel, GPIO.OUT)
        GPIO.output(self._channel, 0)
        sleep(interval)
        self.power_off()
        sleep(interval)

    def power_off(self):
        GPIO.output(self._channel, 1)


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

    scheduler = Scheduler(args.channel)
    schedule.every(args.wait_time).seconds.do(scheduler.power_on_and_off(args.interval))

    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        scheduler.power_off()
        pass


if __name__ == "__main__":
    main()
