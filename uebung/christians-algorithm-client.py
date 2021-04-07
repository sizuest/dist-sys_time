# Python3 program imitating a client process

import socket
import datetime
import time

from dateutil import parser
from localclock import Clock

# Server address
# TODO Passen Sie die Server-IP gemäss den Angaben von der Übungsleitung an
SERVER_IP = '127.0.0.1'

LOCAL_CLOCK = Clock()


def do_measurement():
    s = socket.socket()

    # Server port
    port = 8000

    # connect to the clock server on local computer
    s.connect((SERVER_IP, port))

    request_time = LOCAL_CLOCK.get_time()

    # receive data from the server
    server_time = parser.parse(s.recv(1024).decode())
    response_time = LOCAL_CLOCK.get_time()

    # TODO berechnen Sie die round-trip-time
    # Dafür stehen folgende Variablen zur Verfügung:
    # - request_time: Zeitpunkt des Nachrichtenausgangs (datetime)
    # - response_time: Zeitpunkt des Nachrichteneingangs (datetime)
    round_trip_time = 0

    # synchronize process client clock time
    # TODO berechnen Sie den gemessenen Offset auf basis der Serverzeit, der lokalen Uhr und der round-trip-time
    # Dafür stehen folgende Variablen zur Verfügung:
    # - server_time: Serverzeit (datetime)
    # - response_time: Zeitpunkt des Nachrichteneingangs (datetime)
    # - round_trip_time: round-trip-time (float)
    offset_measurement = 0

    s.close()

    return {"round_trip_time": round_trip_time * 1000000, "offset_measurement": offset_measurement * 1000000}


def get_offset_estimation(m_count=5):
    # TODO Aus mehren Messungen (Anzahl: m_count) soll die beste ausgewählt werden.
    # Die beste Messung ist diejenige, welche die geringste roundtrip-Zeit aufweist.
    best_measurement = do_measurement()

    return best_measurement


# function used to Synchronize client process time
def synchronizeTime():
    try:
        estimation = get_offset_estimation(5)

        # TODO Auf Basis der Schätzung soll die Geschwindigkeit der Uhr angepasst werden
        # Die Uhrengeschwindigkeit kann mittels LOCAL_CLOCK.set_speed(x) auf den Wert x gesetzt werden. x muss grösser als
        # 0 sein. x=1 bedeute nominale Geschwindigkeit
        LOCAL_CLOCK.set_speed(1)

        print("[" + str(Clock().get_time()) + "]: estimated offset: " + str(round(estimation["offset_measurement"])) +
              " us, current clock speed:" + str(round(LOCAL_CLOCK.get_speed() * 100)) + "%", end="\n")
    except Exception as e:
        print("[" + str(Clock().get_time()) + "]: bad string received")

# Driver function
if __name__ == '__main__':

    try:
        # synchronize time using clock server
        while True:
            synchronizeTime()
            time.sleep(5)

    except KeyboardInterrupt:
        print("End")
