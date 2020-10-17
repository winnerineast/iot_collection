import socket
import _thread
import pickle
import ssl
import sys
import time
import psutil
import pyshark
from pyshark.packet.packet import Packet
import paho.mqtt.client as mqtt

####################################################
print('Global configuration area:\n')
MQTT_BROKER_HOSTNAME = '192.168.0.1'
MQTT_BROKER_PORT = 1883
MQTT_BROKER_CONNECTION_TIMOUT = 60
MQTT_BROKER_PACKET_TOPIC_NAME = 'topic/nic'

MQTT_CLIENT_CLEAR_SESSION = True
MQTT_CLIENT_MAX_INFLIGHT_MESSAGES = 80
MQTT_CLIENT_MAX_QUEUED_MESSAGES = 0 # 0 = unlimited
MQTT_CLIENT_MESSAGE_RETRY = 5 # 5 second later to re-send msg
MQTT_CLIENT_DEFAULT_LOGGER = mqtt.MQTT_LOG_ERR
MQTT_CLIENT_CA_CERTS = None # a string path to the Certificate Authority certificate files that are to be treated as trusted by this client.
MQTT_CLIENT_CERTFILE = None #strings pointing to the PEM encoded client certificate and private keys respectively. If these arguments are not None then they will be used as client information for TLS based authentication. Support for this feature is broker dependent. Note that if either of these files in encrypted and needs a password to decrypt it, Python will ask for the password at the command line. It is not currently possible to define a callback to provide the password.
MQTT_CLIENT_KEYFILE = None # as above certfile.
MQTT_CLIENT_CERT_REQS = ssl.CERT_REQUIRED # defines the certificate requirements that the client imposes on the broker. By default this is ssl.CERT_REQUIRED, which means that the broker must provide a certificate.
MQTT_CLIENT_TLS_VERSION = ssl.PROTOCOL_TLS #specifies the version of the SSL/TLS protocol to be used. By default (if the python version supports it) the highest TLS version is detected. If unavailable, TLS v1 is used.
MQTT_CLIENT_CIPHERS = None #a string specifying which encryption ciphers are allowable for this connection, or None to use the defaults.

print("Check whether wireshark is installed.")
####################################################
af_map = {
    socket.AF_INET: 'IPv4',
    socket.AF_INET6: 'IPv6',
    psutil.AF_LINK: 'MAC',
}


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
        client.connected_flag = True  # set flag
    else:
        print("Bad connection Returned code=", rc)
        client.connected_flag = False


def on_disconnect(client, userdata, flags, rc):
    print("Disconnected with result code " + str(rc))
    client.loop_stop()
    client.connected_flag = False


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("====================================================================")
    print("Received - " + msg.topic+" - "+str(msg.payload))


def capture_packet (threadName, nic):
    print("Start an new thread to capture network packets with {}".format(nic))

    client = mqtt.Client(client_id=threadName, clean_session=MQTT_CLIENT_CLEAR_SESSION)
    client.max_queued_messages_set(MQTT_CLIENT_MAX_QUEUED_MESSAGES)
    client.max_inflight_messages_set(MQTT_CLIENT_MAX_INFLIGHT_MESSAGES)
    client.message_retry_set(MQTT_CLIENT_MESSAGE_RETRY)
# Enable it when you have an encrypted MQTT Broker
#    client.tls_set(ca_certs=MQTT_CLIENT_CA_CERTS,
#                   certfile=MQTT_CLIENT_CERTFILE,
#                   keyfile=MQTT_CLIENT_KEYFILE,
#                   cert_reqs=MQTT_CLIENT_CERT_REQS,
#                   tls_version=MQTT_CLIENT_TLS_VERSION,
#                   ciphers=MQTT_CLIENT_CIPHERS
#                   )
#    client.enable_logger(logger=MQTT_CLIENT_DEFAULT_LOGGER)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connected_flag = False

    capture = pyshark.LiveCapture(interface=nic)

    b_connecting_in_progress = False
    while True:
        # When MQTT client has started one connectin, it will wait for successful message back or timout or error
        # without issuing another connection request.
        if b_connecting_in_progress and (not client.connected_flag):
            continue

        try:
            if not client.connected_flag:
                print(f"Connect to MQTT broker {MQTT_BROKER_HOSTNAME}:{MQTT_BROKER_PORT} with keepalive {MQTT_BROKER_CONNECTION_TIMOUT} seconds.")
                client.connect(host=MQTT_BROKER_HOSTNAME, port=MQTT_BROKER_PORT, keepalive=MQTT_BROKER_CONNECTION_TIMOUT)
                client.loop_start()
                b_connecting_in_progress = True
            else:
                i = 0
                for packet in capture.sniff_continuously():
                    print(packet)
                    result = client.publish(MQTT_BROKER_PACKET_TOPIC_NAME, payload=pickle.dumps(packet), qos=0, retain=False)
                    status = result[0]
                    if status == 0:
                        i += 1
                        #print(f"Successfully sent one message {packet}")
                    else:
                        print(f"Failed {result} to send message to topic {MQTT_BROKER_PACKET_TOPIC_NAME}")
                        if status == 4:
                            client.reconnect()
        except ConnectionRefusedError:
            print("ConnectionRefusedError")
            b_connecting_in_progress = False
            time.sleep(MQTT_CLIENT_MESSAGE_RETRY)
            continue
        except KeyboardInterrupt:
            client.disconnect()
            capture.close()
            sys.exit(0)


# List down all network interfaces
for nic, address in psutil.net_if_addrs().items():
    for addr in address:
        if af_map.get(addr.family, addr.family) == 'IPv4':
            if str(addr.address) == '127.0.0.1':
                continue
            try:
                _thread.start_new_thread(capture_packet, (addr.address, nic))
            except:
                print("Error: unable to start thread")
while True:
    pass
