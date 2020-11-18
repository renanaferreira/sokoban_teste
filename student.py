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

async def solver(puzzle, solution):
    while True:
        game_properties = await puzzle.get()
        mapa = Map(game_properties["map"])
        p = SokobanDomain(game_properties["map"])
        initial = {"player": mapa.keeper, "boxes": mapa.boxes}
        goal = {"boxes": mapa.filter_tiles([Tiles.MAN_ON_GOAL, Tiles.BOX_ON_GOAL, Tiles.GOAL])}
        problema = SearchProblem(p, initial, goal)
        t = SearchTree(problema, 'a*', mapa)
        print(mapa)

        while True:
            t.search()
            await asyncio.sleep(0)  # this should be 0 in your code and this is REQUIRED
            break

        keys = t.get_plan(t.solution)
        #print(keys)
        await solution.put(keys)

async def agent_loop(puzzle, solution, server_address="localhost:8001", agent_name="student"):
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
                    keys = ""
                    await puzzle.put(game_properties)

                if not solution.empty():
                    keys = await solution.get()
                    print(keys)

                key = ""
                if len(keys):  # we got a solution!
                    key = keys[0]
                    keys = keys[1:]

                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8001")
NAME = os.environ.get("NAME", getpass.getuser())

puzzle = asyncio.Queue(loop=loop)
solution = asyncio.Queue(loop=loop)

net_task = loop.create_task(agent_loop(puzzle, solution, f"{SERVER}:{PORT}", NAME))
solver_task = loop.create_task(solver(puzzle, solution))

loop.run_until_complete(asyncio.gather(net_task, solver_task))
loop.close()