# ZMQ-Adapter

This is an example ZMQ adapter.
It simply forwards all messages between the ClearBlade platform and a few ZMQ speaking nodes. 

## Prereqs
- [ClearBlade Python SDK](https://pypi.org/project/clearblade/)
- [ZMQ](http://zeromq.org/intro:get-the-software)
- [PyZMQ](http://zeromq.org/bindings:python)

## Running the example

Open up three terminal windows.

First, edit the `zmq_adapter.py` script with your system's credentials.
Start it up in the first window and make sure it connects without error.
The adapter will connect to the ClearBlade platform's MQTT broker and start publishing all received MQTT messages over ZMQ on localhost:5556.
It will also connect to any addresses in the `zmq_clients` variable over ZMQ and forward all messages published from them to the MQTT broker.

In the example directory, there are two scripts.

- `zmq_publisher.py` - publishes the current time over ZMQ on localhost:5557
- `zmq_subscriber.py` - subscribes to the "time" topic via ZMQ at localhost:5556 (the adapter)

Run them in your two remaining windows.
The publisher won't output anything, but you should see the messages being relayed to and from the platform via the `zmq_adapter.py` logs.
When you start the `zmq_subscriber.py` script, you will start seeing the current time logs show up every second. 
You will also see them show up in the ClearBlade platform, if you subscribe to the `time` topic in the messaging panel of your system.
