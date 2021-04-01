# Simple implementation of a local clock
import datetime
from random import random, randint

class Clock:

    def __init__(self):
        self._time = datetime.datetime.now() + datetime.timedelta(seconds=randint(-10, 10))
        self._speed = 1
        self._static_speed_error = 1 - (random() - .5) / 50
        self._last_read = datetime.datetime.now()

    def get_time(self):

        time_difference = datetime.datetime.now() - self._last_read
        self._last_read = datetime.datetime.now()

        time_leap = time_difference.total_seconds() * self._speed * self._static_speed_error

        self._time += datetime.timedelta(seconds=time_leap)

        return self._time

    def set_speed(self, new_speed):
        self._speed = max(0.01, new_speed)

    def get_speed(self):
        return self._speed
