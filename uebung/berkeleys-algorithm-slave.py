# Python3 program imitating a client process

import threading
import datetime
import socket
import time
from random import randint, random
from localclock import Clock
import sys
import logging
import signal

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-9s) %(message)s', )

# Server address
# TODO Passen Sie die Server-IP gemäss den Angaben von der Übungsleitung an
SERVER_IP = '127.0.0.1'

# Clock settings (random initialization)
LOCAL_CLOCK = Clock()

# client thread function used to send time at client side
def startSendingTime(slave_client):
    while True:
        if stop_event.is_set():
            slave_client.close()
            logging.debug('Exiting - startSendingTime')
            break
        try:
            # provide server with clock time at the client
            # TODO Lesen Sie die aktuelle Zeit aus der Uhr (LOCAL_CLOCK)
            time_str = str(0)
            slave_client.send(time_str.encode())
            print("[" + time_str + "]: current time sent successfully", end="\n")
            time.sleep(5)

        except socket.error as e:
            print("Connection error: %s" % e)
            logging.debug("Exit sending, socket error")
            break


# client thread function used to receive synchronized time
def startReceivingTime(slave_client):
    while True:
        try:
            if stop_event.is_set():
                slave_client.close()
                logging.debug('Exiting - startReceivingTime')
                break
            # receive data from the server
            estimated_offset_in_seconds_string = slave_client.recv(1024).decode()
            estimated_offset_in_seconds = float(estimated_offset_in_seconds_string)

            # TODO Auf Basis der Schätzung soll die Geschwindigkeit der Uhr angepasst werden
            # Die Uhrengeschwindigkeit kann mittels LOCAL_CLOCK.set_speed(x) auf den Wert x gesetzt werden. x muss grösser
            # als 0 sein. x=1 bedeute nominale Geschwindigkeit
            LOCAL_CLOCK.set_speed(1)

            print("[" + str(Clock().get_time()) + "]: estimated offset: " + str(round(estimated_offset_in_seconds*1000)/1000) +
                " s, current clock speed:" + str(round(LOCAL_CLOCK.get_speed()*100)) + "%", end="\n")

        except socket.error as e:
            print("Connection error: %s" % e)
            logging.debug("Exit receiving, socket error")
            break
        except Exception as e:
            print("[" + str(Clock().get_time()) + "]: bad string received")
            logging.debug("Exit receiving, string error")
            break

# function used to Synchronize client process time
def initiateSlaveClient(port):
    slave_client = socket.socket()

    # connect to the clock server on local computer
    slave_client.connect((SERVER_IP, port))

    # start sending time to server
    print("Starting to receive time from server\n")
    send_time_thread = threading.Thread(target=startSendingTime, args=(slave_client,), name="sender_thread")
    send_time_thread.start()

    # start receiving synchronized from server
    print("Starting to receiving " + "synchronized time from server\n")
    receive_time_thread = threading.Thread(target=startReceivingTime, args=(slave_client,), name="receiver_thread")
    receive_time_thread.start()

def handle_kb_interrupt(sig, frame):
    stop_event.set()
    time.sleep(5)
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug("start joining: " + str(t))
        t.join(1)
        logging.debug("joined or killed: " + str(t))
    sys.exit()

# Driver function
if __name__ == '__main__':
    stop_event = threading.Event()
    signal.signal(signal.SIGINT, handle_kb_interrupt)
    # initialize the Slave / Client
    initiateSlaveClient(port=8080)
    while True:
        time.sleep(10)
