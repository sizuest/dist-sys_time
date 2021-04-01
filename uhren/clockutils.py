# General classes to represent processes with clock exchanging messages
# Date: 07.01.2021
# Author: ZuS
from abc import ABC, abstractmethod


# ======================================================================================================
# General abstract class for a clock
class Clock(ABC):

    # to be executed before an event is handled
    @abstractmethod
    def pre_event(self):
        pass

    # to be executed after a message has been received
    @abstractmethod
    def post_receive(self, time):
        pass

    # returns the current reading as string. A minimum length of the string can be stated
    @abstractmethod
    def to_string(self,  fill=0):
        pass

    # checks whether the current clock reading is equal to the provided reference
    @abstractmethod
    def is_equal(self, ref):
        pass

    # checks whether the current clock reading is smaller than the provided reference
    @abstractmethod
    def is_less(self, ref):
        pass

    # returns a timestamp
    @abstractmethod
    def get_timestamp(self):
        pass

    # states whether or not the clock is able to evaluate the HBR
    @abstractmethod
    def can_do_happened_before_relation(self):
        pass


# ======================================================================================================
# Implementation of a logic clock
class LogicClock(Clock):

    def __init__(self, pid):
        self.pid = pid
        self.clock_value = 0

    def pre_event(self):
        self.clock_value += 1

    def post_receive(self, time):
        # sync clocks
        self.clock_value = max(self.clock_value, time)

    def to_string(self, min_length=0):
        str_out = str(self.clock_value)

        if len(str_out) < min_length:
            str_out = " " * (min_length - len(str_out)) + str_out

        return str_out

    def is_less(self, ref: 'LogicClock'):
        if self.is_equal(ref):
            return self.pid < ref.pid

        return self.clock_value < ref.clock_value

    def is_equal(self, ref: 'LogicClock'):
        return self.clock_value == ref.clock_value

    def get_timestamp(self):
        return self.clock_value

    def can_do_happened_before_relation(self):
        return False


# ======================================================================================================
# Implementation of a vector clock
class VectorClock(Clock):
    def __init__(self, p_count, pid):
        self.pid = pid
        self.clock_value = []
        for i in range(0, p_count):
            self.clock_value.append(0)

    def pre_event(self):
        self.clock_value[self.pid] += 1

    def post_receive(self, time):
        # merge clocks
        for i in range(0, len(self.clock_value)):
            self.clock_value[i] = max(self.clock_value[i], time[i])

    def to_string(self, fill=0):
        str_out = "["

        for i in self.clock_value:
            str_i = str(i)
            if len(str_i) < fill:
                str_i = " " * (fill - len(str_i)) + str_i

            str_out += str_i + ", "

        str_out = str_out[:-2] + "]"

        return str_out

    def is_less(self, ref: 'VectorClock'):
        if self.is_equal(ref):
            return False

        for i in range(0, len(self.clock_value)):
            if self.clock_value[i] > ref.clock_value[i]:
                return False

        return True

    def is_equal(self, ref: 'VectorClock'):
        for i in range(0, len(self.clock_value)):
            if self.clock_value[i] != ref.clock_value[i]:
                return False

        return True

    def get_timestamp(self):
        return self.clock_value.copy()

    def can_do_happened_before_relation(self):
        return True


# ======================================================================================================
# General message including the message and its timestamp
class Message:

    def __init__(self, message, time):
        self.message = message
        self.time = time

    def get_message(self):
        return self.message

    def get_time(self):
        return self.time


# ======================================================================================================
# General process including a clock, an event handler and a message handler
class Process:

    def __init__(self, name: str, clock: Clock):
        self.clock = clock
        self.name = name
        self.last_event = ""

    def new_message(self, m):
        return Message(m, self.get_clock().get_timestamp())

    def handle_event(self, event):
        self.clock.pre_event()
        return event

    def handle_message(self, message: Message):
        # sync clocks
        self.clock.post_receive(message.get_time())
        # Raise an event to process the message
        return self.handle_event(self.get_name()+": "+message.get_message())

    def get_name(self):
        return self.name

    def get_clock(self):
        return self.clock
