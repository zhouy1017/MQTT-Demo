import robot_comm
import random
import time
import asyncio
import signal
import os
import uvloop
import glb
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

STOP = asyncio.Event()
HOST_ADDR = '127.0.0.1'
def ask_exit(*args):
    STOP.set()
def create_identifier(data):
    i = 0
    while i in glb.mem.keys():
        i = random.randrange(10000)
    glb.mem[i] = data
    return i 
    
async def main(host,token):
    client = robot_comm.prepare_client(token)
    client.set_auth_credentials(token, None)
    await client.connect(host)
    random.seed()
    target = "pm_clients/" + client._client_id + "/task1/requests" 

    for i in range(10):
        r = str(random.randrange(1000))
        id = create_identifier(r)
        id_format = '{:0>4}'.format(str(id))
        req = id_format + str(r)
        client.publish(target,req,qos=0)


    await STOP.wait()
    await client.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    token = 'gg121'

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main(HOST_ADDR, token))