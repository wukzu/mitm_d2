import asyncio
import websockets

import threading

webso = None

async def test():
    await webso.send("aaaaa")

async def hello(websocket, path):
    webso = websocket
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "localhost", 8888)

a = asyncio.get_event_loop()



asyncio.get_event_loop().run_until_complete(start_server)

a = asyncio.get_event_loop()

t1 = threading.Thread(target=a.run_forever, args=())

t1.start()

for x in range(60000000000):
    if x == 10000:
        await test()