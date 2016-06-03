# ZMQ-Adapter
This is an ZMQ adapter for MQTT written in Python. It is designed internally to connect to the ClearBlade MQTT Broker. It provides two types of adaptations:
1.  ZMQ to MQTT(adapter/zmq2mqtt.py):
    *   ZMQ publishes are sent over to MQTT broker under the topic "zmq/publish".
2.  MQTT to ZMQ(adapter/mqtt2zmq.py):    
    *   MQTT publishes on topic "zmq/subscribe" are sent over the bound tcp address of ZMQ SUB.

IMPORTANT: The messages sent by MQTT publisher are added "1#" at the start of every message. Therefore, the messages received by ZMQ SUB always start with "1#".

NOTE: This adapter is still in beta and only supports PUB, SUB functionality of the ZMQ protocol.

## Installation
*   Clone this repository
*   You will need to have Eclipse Paho library for Python, installed on your system. Please follow instructions given at https://eclipse.org/paho/clients/python/ or https://pypi.python.org/pypi/paho-mqtt/1.1
*   Clone the clearblade Python-API repository from https://github.com/ClearBlade/Python-API. It is the Python SDK for ClearBlade.
*   Use the README.md to install the Python SDK for ClearBlade.
*   Install ZMQ library on your machine from http://zeromq.org/intro:get-the-software.
*   Install ZMQ Python binding from http://zeromq.org/bindings:python.
*   You can start the adapter by running the required adpter python script
*   You can enter the bind address of ZMQ PUB and connect address of ZMQ SUB in the main() functions of both the adapter Python scripts.

## Usage
### Using zmq2mqtt adapter
There are 2 files from this repo in picture for this scenario.
1.  zmq2mqtt.py
2.  pub.py

zmq pub
```Python
import zmq
import time
import clearblade
from clearblade import auth
from clearblade import Client
from clearblade import Messaging

bindAddress = "tcp://127.0.0.1:7777"    #Specify your own bind address

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
```

zmq2mqtt
```Python
import paho.mqtt.client as mqtt
import thread
import time
from clearblade import Client
from clearblade import UserClient 
import string
from clearblade import auth
from clearblade import Messaging
import zmq

class zmq2mqtt():

	def __init__(self, userClient, bindAddress):
		self.userClient = userClient
		self.bindAddress = bindAddress
		self.auth = auth.Auth()
		self.auth.Authenticate(self.userClient)
		self.message = Messaging.Messaging(self.userClient)
		self.status = self.message.InitializeMQTT()
		self.zmqSub(self.message, self.bindAddress)
		

	def zmqSub(self, message, bindAddress):
		pass
		# ZeroMQ Context
		context = zmq.Context()

		# Define the socket using the "Context"
		sock = context.socket(zmq.SUB)

		# Define subscription and messages with prefix to accept.
		sock.setsockopt(zmq.SUBSCRIBE, "1")
		sock.connect(str(self.bindAddress))

		while True:
		    recMessage= sock.recv()
		    print "Your message is "+recMessage
		    self.mqttPub(recMessage)

    	def mqttPub(self, message):
    		self.message.publishMessage("zmq/publish", str(message), 1)


if __name__ == '__main__':
	userClient = Client.UserClient("CLEARBLADE_SYSTEM_KEY", "CLEARBLADE_SYSTEM_SECRET", "CLEARBLADE_USER_EMAIL", "CLEARBLADE_USER_PASSWORD", "CLEARBLADE_PLATFORM_URL") 
	bindAddress = "tcp://127.0.0.1:7777"    #ZMQ Bind address
	zmq2mqtt = zmq2mqtt(userClient, bindAddress)
```
*   Replace the CLEARBLADE-SYSTEM_KEY, CLEARBLADE_SYSTEM_SECRET, CLEARBLADE_USER_EMAIL, CLEARBLADE_USER_PASSWORD & CLEARBLADE-PLATFORM_URL, with your own. An example of the CLEARBLADE-PLATFORM_URL can be platform.clearblade.com.
*   Run both the python scripts.
*   You will see the messages getting published on "zmq/publish" on your MQTT broker.

### Using mqtt2zmq adapter
There are 2 files from this repo in picture for this scenario.

1.  mqtt2zmq.py
2.  sub.py

zmq sub

```Python
import zmq
import time

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.SUB)

# Define subscription and messages with prefix to accept.
sock.setsockopt(zmq.SUBSCRIBE, "1")
sock.connect("tcp://127.0.0.1:7777")    #Specify your own binding address

while True:
    message= sock.recv()
    print message
```

mqtt2zmq
```Python
import paho.mqtt.client as mqtt
import thread
import time
from clearblade import Client
from clearblade import UserClient 
import string
from clearblade import auth
from clearblade import Messaging
import zmq

class mqtt2zmq():

	def __init__(self, userClient, bindAddress):
		self.userClient = userClient
		self.bindAddress = bindAddress
		self.auth = auth.Auth()
		self.auth.Authenticate(self.userClient)
		self.message = Messaging.Messaging(self.userClient)
		self.message.printValue()
		self.status = self.message.InitializeMQTT(keep_alive=60)
		context = zmq.Context()

		# Define the socket using the "Context"
		self.sock = context.socket(zmq.PUB)
		print "Bind Address is "+bindAddress
		self.sock.bind(bindAddress)
		self.mqttSub(self.message,self.sock)

	def mqttSub(self, message, sock):
		time.sleep(1)

		def onMessageCallback(client, obj, msg):
			print "Your message is : "+msg.payload
			data = msg.payload
			self.ZmqPub(data, self.sock)

		message.subscribe("zmq/subscribe", 1, onMessageCallback)
		while True:
			pass

	def ZmqPub(self, data, sock):
		time.sleep(1)
		message = "1#"+data
		self.sock.send(message)

if __name__ == '__main__':
	userClient = Client.UserClient("CLEARBLADE_SYSTEM_KEY", "CLEARBLADE_SYSTEM_SECRET", "CLEARBLADE_USER_EMAIL", "CLEARBLADE_USER_PASSWORD", "CLEARBLADE_PLATFORM_URL")  
	bindAddress = "tcp://127.0.0.1:7777"
	mqtt2zmq = mqtt2zmq(userClient, bindAddress)
```
*   Replace the CLEARBLADE-SYSTEM_KEY, CLEARBLADE_SYSTEM_SECRET, CLEARBLADE_USER_EMAIL, CLEARBLADE_USER_PASSWORD & CLEARBLADE-PLATFORM_URL, with your own. An example of the CLEARBLADE-PLATFORM_URL can be platform.clearblade.com.
*   Run both the python scripts.
*   MQTT messages published on "zmq/subscribe" are now published to ZMQ and you can see them on the console of "sub.py". The actual MQTT message start after "1#".


