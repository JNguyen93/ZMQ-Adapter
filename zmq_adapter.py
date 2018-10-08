from clearblade.ClearBladeCore import System
import zmq

###############################
##        Config time        ##
###############################

# Which MQTT topics do you want to forward?
# (for all, use pound sign: "#")
mqtt_incoming_subscriptions = [
    "#"
]

# Which ZMQ topics do you want to forward?
# (for all, use empty string: "")
zmq_incoming_subscriptions = [
    ""
]

# How is the ZMQ message separated from the topic?
zmq_topic_delimiter = "::"

# Where should ZMQ be publishing?
# We'll bind to this port for subscribers to connect to
zmq_bind_address = "tcp://127.0.0.1:5556"

# Where are your ZMQ clients?
# We'll connect to these ports and subscribe
zmq_clients = [
    "tcp://127.0.0.1:5557",
    "tcp://127.0.0.1:5558"
]

# What are your ClearBlade credentials?
# FILL THESE IN WITH YOUR CREDENTIALS!!
cb_url = "https://platform.clearblade.com"
system_key = ""
system_secret = ""
email = ""
password = ""

################################
##        Adapter time        ##
################################

# Set up ZMQ publisher connection
pub_context = zmq.Context()
zmq_pub_sock = pub_context.socket(zmq.PUB)
zmq_pub_sock.bind(zmq_bind_address)

# Set up ZMQ subscriber connection
sub_context = zmq.Context()
zmq_sub_sock = sub_context.socket(zmq.SUB)

# Set up MQTT connection
zmq_system = System(system_key, system_secret, cb_url)
zmq_user = zmq_system.User(email, password)
mqtt = zmq_system.Messaging(zmq_user, client_id="zmq_tester")
mqtt_connected = False


# When we connect, subscribe to all topics in our subscriptions array
def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    mqtt_connected = True
    for topic in mqtt_incoming_subscriptions:
        client.subscribe(topic)


# When we receive a message, forward it via ZMQ
def on_message(client, userdata, message):
    zmq_message = "{}{}{}".format(message.topic, zmq_topic_delimiter, message.payload)
    zmq_pub_sock.send_string(zmq_message)


# Let's try to reconnect if we disconnect
def on_disconnect(client, userdata, rc):
    global mqtt_connected
    mqtt_connected = False
    global mqtt
    mqtt.connect()


# Connect callbacks to client and connect
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.on_disconnect = on_disconnect
mqtt.connect()

# Set ZMQ subscriptions
for topic in zmq_incoming_subscriptions:
    try:
        sock.setsockopt(zmq.SUBSCRIBE, b'value')
    except TypeError:
        sock.setsockopt_string(zmq.SUBSCRIBE, b'value')


# Connect to ZMQ clients
for client in zmq_clients:
    zmq_sub_sock.connect(client)

# Wait for ZMQ messages to come in, then forward via MQTT
while True:
    # We assume ascii messages only in this adapter
    # If you want binary messages, code it yourself
    message = zmq_sub_sock.recv().decode('ascii')

    # Separate message from topic by the delimiter we defined above
    split_message = message.split(zmq_topic_delimiter)
    topic = split_message[0]

    # Rejoin in case delimiter appeared multiple times in the message
    # We assume the _first_ occurance separates the topic
    mqtt_message = zmq_topic_delimiter.join(split_message[1:])

    # Only forward if we're currently connected
    if mqtt_connected:
        mqtt.publish(topic, mqtt_message)
