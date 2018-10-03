import zmq

context = zmq.Context()
sock = context.socket(zmq.SUB)
sock.setsockopt_string(zmq.SUBSCRIBE, "time")
sock.connect("tcp://127.0.0.1:5556")

# Prints out all messages published on the `time` topic
while True:
    message = sock.recv().decode('ascii')
    print(message)
