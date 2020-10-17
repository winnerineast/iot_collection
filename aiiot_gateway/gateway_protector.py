import time
import paho.mqtt.client as mqtt
import pickle
from pyshark.packet.packet import Packet


####################################################
print('Global configuration area:\n')
MQTT_BROKER_HOSTNAME = '192.168.1.118'
MQTT_BROKER_PORT = 1883
MQTT_BROKER_CONNECTION_TIMOUT = 60
MQTT_BROKER_PACKET_TOPIC_NAME = 'topic/nic'

print("Check whether wireshark is installed.")
####################################################


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
        client.connected_flag = True  # set flag
    else:
        print("Bad connection Returned code=", rc)


# The callback for when the client receives a CONNACK response from the server.
def on_disconnect(client, userdata, flags, rc):
    print("Disconnected with result code " + str(rc))
    client.loop_stop()


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    packet = pickle.loads(msg.payload)

    # ignore all MQTT messages
    tcp_source_port = packet.get_multiple_layers("TCP")[0].get_field_by_showname('Source Port')
    tcp_destination_port = packet.get_multiple_layers("TCP")[0].get_field_by_showname('Destination Port')
    if tcp_source_port == '1883' or tcp_destination_port == '1883':
        return
    else:
        print(f"Found security issue with tcp port {tcp_source_port}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connected_flag = False

while True:
    try:
        if not client.connected_flag:
            print(
                "Connect to MQTT broker {}:{} with keepalive {} seconds.".format(
                    MQTT_BROKER_HOSTNAME,
                    MQTT_BROKER_PORT,
                    MQTT_BROKER_CONNECTION_TIMOUT))
            client.connect(MQTT_BROKER_HOSTNAME, MQTT_BROKER_PORT, MQTT_BROKER_CONNECTION_TIMOUT)
            client.loop_start()
            client.subscribe(MQTT_BROKER_PACKET_TOPIC_NAME, qos=0)
            client.connected_flag = True
        else:
            time.sleep(5)
    except Exception as e:
        print(e)