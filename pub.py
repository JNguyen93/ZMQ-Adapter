import zmq
import time
import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging

bindAddress = "tcp://127.0.0.1:7777"

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.PUB)
print "Bind Address is "+bindAddress
sock.bind(bindAddress)

id = 0

while True:
    time.sleep(1)
    id, now = id+1, time.ctime()

    # Message [prefix][message]
    message = "1-Update! No. #"+str(id)+" at "+now
    sock.send(message)

    id += 1
