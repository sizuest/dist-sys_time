# General class representing a process with a logical clock
# Date: 07.01.2021
# Author: ZuS

class Process:

    def __init__(self, name, init_value=0):
        self.value = init_value
        self.name = name

    def handle_event(self, event):
        self.value += 1

    def handle_message(self, message):
        self.value = max(self.value, message.get_time())

    def get_name(self):
        return self.name

# General class representing a message with a logical time stamp
# Date: 07.01.2021
# Author: ZuS


class Message:

    def __init__(self, message, time):
        self.message = message
        self.time = time

    def get_message(self):
        return self.message

    def get_time(self):
        return self.time




