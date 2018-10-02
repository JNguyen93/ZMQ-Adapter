import zmq
import time

bind_address = "tcp://127.0.0.1:5557"
context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind(bind_address)

# Publishes the current time every second
while True:
    message = "time::" + time.ctime()
    sock.send_string(message)
    time.sleep(1)
