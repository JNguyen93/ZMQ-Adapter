import zmq

context = zmq.Context()
sock = context.socket(zmq.SUB)
try:
    sock.setsockopt(zmq.SUBSCRIBE, b'time')
except TypeError:
    sock.setsockopt_string(zmq.SUBSCRIBE, b'time')
sock.connect("tcp://127.0.0.1:5556")

# Prints out all messages published on the `time` topic
while True:
    message = sock.recv().decode('ascii')
    print(message)
