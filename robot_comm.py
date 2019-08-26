import os
import signal
import time
import uuid
import glb
import handler
from gmqtt import Client as MQTTClient

HOST_ADDR = '127.0.0.1'


# Use mac addr + time to create unique clientid
# TODO suggest to implenment blacklist on server side to prevent clientid conflict
# in very rare occasions or malicious attack 
def create_uid():
    return "".join(str(uuid.uuid4()).split('-'))


def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('clients/#', qos=0)
    pm = 'pm_clients/' + client._client_id + '/#'
    client.subscribe(pm,qos=0)


def on_message(client, topic, payload, qos, properties):
    payload = bytes.decode(payload,'utf-8')
    handler.handle(client,topic,payload,glb.mem)


def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos):
    print('SUBSCRIBED')


def prepare_client(token):
    CLIENT_ID = create_uid()

    client = MQTTClient(CLIENT_ID)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    client.set_auth_credentials(token, None)

    return client
