import asyncio
import getpass
import json
import os
import random
import websockets
from mapa import Map

class Client:
    def __init__(self, addr, name):
        self.server_address=addr
        self.agent_name=name

    async def agent_loop(self, server_address, agent_name):
        async with websockets.connect(f"ws://{server_address}/player") as websocket:
            # Receive information about static game properties
            await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

            while True:
                try:
                    update = json.loads(
                        await websocket.recv()
                    )  # receive game update, this must be called timely or your game will get out of sync with the server

                    if "map" in update:
                        # we got a new level
                        game_properties = update
                        mapa = Map(update["map"])
                    else:
                        # we got a current map state update
                        state = update
                    
                    # BRUTE FORCE GAMING : obviously not working by: andre
                    lado=random.random()
                    if lado<=0.25:
                        key="w"
                    elif lado<=0.5:
                        key="d"
                    elif lado<=0.75:
                        key="s"
                    else:
                        key="a"
                    
                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )
                except websockets.exceptions.ConnectionClosedOK:
                    print("Server has cleanly disconnected us")
                    return

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
if __name__=="__main__":
    c=Client("localhost:8000", "student")
    loop = asyncio.get_event_loop()
    SERVER = os.environ.get("SERVER", "localhost")
    PORT = os.environ.get("PORT", "8000")
    NAME = os.environ.get("NAME", getpass.getuser())
    loop.run_until_complete(c.agent_loop(f"{SERVER}:{PORT}", NAME))
