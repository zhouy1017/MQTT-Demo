import asyncio
import os
import signal
import time
import uuid
from gmqtt import Client as MQTTClient
import uuid
import uvloop
import threading
HOST_ADDR = '127.0.0.1'
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

STOP = asyncio.Event()
online_clients = []
# create unique id for client and the SysClient will have 'Sys' as prefix
def create_uid():
    s = "".join(str(uuid.uuid4()).split('-'))
    return 'Sys' + s

def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('$SYS/brokers/emqx@127.0.0.1/#', qos=0)
    client.subscribe('clients/#',qos=0)
    client.subscribe('pm_clients/#',qos=0)


def on_message(client, topic, payload, qos, properties):
    request_handler(client,topic,payload)

def request_handler(client,topic,payload):

    # This part of code simulates how server handles the requests from clients
    asyncio.sleep(2) # simulates the computing time
    topic_s = topic.split('/')
    payload_s = bytes.decode(payload,'utf-8')
    if topic_s[2] == 'task1' and topic_s[3] == 'requests':
        
        data = payload_s[4:]
        number = int(data)
        mark = None
        if number < 330:
            mark = 'A'
        elif number < 660:
            mark = 'B'
        else:
            mark = 'C'
        res = payload_s[:4] + mark
        target = "/".join(topic_s[0:3]) + '/responses'
        client.publish(target,res,qos=0)

    # This part of code monitors the connect/disconnect of the clients
    if "/".join(topic_s[:4]) == "$SYS/brokers/emqx@127.0.0.1/clients":
        if topic_s[5] == 'connected':
            # new client connect
            client_id = topic_s[4]
            if client_id not in online_clients:
                online_clients.append(client_id)
            else:
                # TODO Wait to be clarified how to deal with this case
                print("Error! The client is already online!")
        if topic_s[5] == 'disconnected':
            client_id = topic_s[4]
            if client_id not in online_clients:
                 # TODO Wait to be clarified how to deal with this case
                print("Error! The client is already online!")   
            else:
                online_clients.remove(client_id)         

def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos):
    print('SUBSCRIBED')

def ask_exit(*args):
    STOP.set()

def watchdog_clients():
    while True:
        time.sleep(5)
        print("Clients_Online: ", online_clients)

async def main(broker_host, token):
    client_id = create_uid()
    client = MQTTClient(client_id)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    
    client.set_auth_credentials(token, None)
    await client.connect(broker_host)

    # Watchdog print out online_clients every 5s
    t = threading.Thread(target = watchdog_clients)
    t.setDaemon(True)
    t.start()

    await STOP.wait()
    await client.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    token = 'SysClient'

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main(HOST_ADDR, token))
