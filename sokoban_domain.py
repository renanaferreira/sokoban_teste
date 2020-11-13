from tree_search import *
from math import hypot
from mapa import Map
from consts import Tiles, TILES
from copy import deepcopy

def minimal_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return hypot(x1-x2, y1-y2)

class SokobanDomain(SearchDomain):
    def __init__(self, filename):
        self.change_map(filename)

    def change_map(self, filename):
        self.level = filename
        self.map = Map(filename)
        self.map.clear_tile(self.map.keeper)
        boxs = self.map.boxes
        for box in boxs:
            self.map.clear_tile(box)

    def instantiate_map(self, state):
        mapa = deepcopy(self.map)
        for box in state["boxes"]:
            mapa.set_tile(box, Tiles.BOX)
        mapa.set_tile(state["player"], Tiles.MAN)
        return mapa

    def get_state(self, mapa):
        if(mapa is None):
            return None
        return {"player": mapa.keeper, "boxes": mapa.boxes}

    def move(self, mapa, cur, direction):
        """Move an entity in the game."""
        assert direction in "wasd", f"Can't move in {direction} direction"

        cx, cy = cur
        ctile = mapa.get_tile(cur)

        npos = cur
        if direction == "w":
            npos = cx, cy - 1
        if direction == "a":
            npos = cx - 1, cy
        if direction == "s":
            npos = cx, cy + 1
        if direction == "d":
            npos = cx + 1, cy

        # test blocked
        if mapa.is_blocked(npos):
            return None
        if mapa.get_tile(npos) in [Tiles.BOX,Tiles.BOX_ON_GOAL,]:  # next position has a box?
            if ctile & Tiles.MAN == Tiles.MAN:  # if you are the keeper you can push
                newmap = self.move(mapa, npos, direction)
                if newmap is None:  # as long as the pushed box can move
                    return None
                mapa = newmap # I am afraid I was passing by value
            else:  # you are not the Keeper, so no pushing
                return None

        # actually update map
        mapa.set_tile(npos, ctile)
        mapa.clear_tile(cur)
        
        return mapa

    def trapped(self, state):
        if(state is None):
            return False
        mapa = self.instantiate_map(state)
        for box in state["boxes"]:
            if box in self.map.empty_goals:
                continue
            (x, y) = box

            pos_m_n=(x-1, y)
            pos_n_m=(x, y-1)
            if mapa.is_blocked(pos_m_n) and mapa.is_blocked(pos_n_m):
                return True

            pos_p_n=(x+1, y)
            pos_n_p=(x, y+1)
            if mapa.is_blocked(pos_p_n) and mapa.is_blocked(pos_n_p):
                return True

            pos_p_n=(x+1, y)
            pos_n_m=(x, y-1)
            if mapa.is_blocked(pos_p_n) and mapa.is_blocked(pos_n_m):
                return True

            pos_m_n=(x-1, y)
            pos_n_p=(x, y+1)
            if mapa.is_blocked(pos_m_n) and mapa.is_blocked(pos_n_p):
                return True
        return False

    def actions(self,state):
        return ["w", "a", "s", "d"]

    def result(self,state,action):
        mapa = self.instantiate_map(state)
        newstate = self.get_state(self.move(mapa,state["player"], action))
        if(self.trapped(newstate)):
            return None
        return newstate
        
    def cost(self, state, action):
        return 1

    def heuristic(self, state, goal): 
        return 0

    def satisfies(self, state, goal):
        mapa = self.instantiate_map(state)
        return mapa.completed
