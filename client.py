import asyncio
import getpass
import json
import os
import random
import websockets
from mapa import Map
from tree_search import *
import mapa
from sokoban_domain import SokobanDomain
from consts import Tiles, TILES

class Client:
    def __init__(self, addr, name):
        self.server_address=addr
        self.agent_name=name
        self.plan = None

    def sokobanSolver(self, filename):
        p = SokobanDomain(filename)
        mapa = Map(filename)
        initial = {"player": mapa.keeper,"boxes": mapa.boxes}
        goal = {"boxes": mapa.filter_tiles([Tiles.MAN_ON_GOAL, Tiles.BOX_ON_GOAL, Tiles.GOAL])}
        problema = SearchProblem(p, initial, goal)
        return SearchTree(problema, 'depth')

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
                        solver = self.sokobanSolver(update["map"])
                        p = solver.search()
                        if(p is None):
                            break
                        self.plan = solver.get_plan(solver.solution)
                        print(self.plan)
                    else:
                        # we got a current map state update
                        state = update
                    
                    if self.plan == []:
                        break
                    key = self.plan[0]
                    self.plan = self.plan[1:]
                    
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
    
