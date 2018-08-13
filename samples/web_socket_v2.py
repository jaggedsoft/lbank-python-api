#!/usr/bin/env python

'''
Subscribe data from LBank websocket server.
A websockets package was required. Please visit 
https://websockets.readthedocs.io/en/stable/intro.html
for more details.
'''

import asyncio
from json import loads as load_json, dumps as dump_json
from time import sleep

import websockets

async def hello(uri):
    print (uri)
    async with websockets.connect(uri) as websocket:
        
        # Subscribe KBar
        data = {'action': 'subscribe', 'subscribe': 'kbar', 'kbar': '5min', 'pair': 'eth_btc'}
        data = dump_json(data)
        await websocket.send(data)

        sleep(0.1)
        # Subscribe Trade
        data = {'action': 'subscribe', 'subscribe': 'trade', 'pair': 'eth_btc'}
        data = dump_json(data)
        await websocket.send(data)

        sleep(0.1)
        # Subscribe Depth
        data = {'action': 'subscribe', 'subscribe': 'depth', 'depth': 10, 'pair': 'eth_btc'}
        data = dump_json(data)
        await websocket.send(data)
        
        sleep(0.1)
        # Subscribe Tick
        data = {'action': 'subscribe', 'subscribe': 'tick', 'pair': 'eth_btc'}
        data = dump_json(data)
        await websocket.send(data)

        async for message in websocket:
            message = load_json(message)
            if 'ping' in message:
                data = {'action': 'pong', 'pong': message['ping']}
                await websocket.send(dump_json(data))
            else:
                print (message)


asyncio.get_event_loop().run_until_complete(
    hello('ws://api.lbank.info/ws/V2/')   # Beyond the wall
)

