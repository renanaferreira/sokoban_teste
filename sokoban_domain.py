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

    def move(self, mapa, cur, action):        
        ctile = mapa.get_tile(cur)
        npos = mapa.new_pos(cur, action)
        if mapa.is_blocked(npos):
            return None
        if mapa.is_box(npos):  
            if mapa.is_man_2(ctile):  
                newmap = self.move(mapa, npos, action)
                if newmap is None:  
                    return None
                mapa = newmap 
            else:  
                return None
        mapa.set_tile(npos, ctile)
        mapa.clear_tile(cur)
        return mapa

    def move2(self, mapa, action):      
        player =  mapa.keeper
        npos = mapa.new_pos(player, action)
        if mapa.is_blocked(npos):
            return None
        if mapa.is_box(npos):
            npos2 = mapa.new_pos(npos, action)
            if mapa.is_blocked(npos2) or mapa.is_box(npos2):
                return None
            mapa.set_tile(npos2, Tiles.BOX)
            mapa.clear_tile(npos)
        mapa.move_man(npos)
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
        #newstate = self.get_state(self.move(mapa,state["player"], action))
        newstate = self.get_state(self.move2(mapa, action))
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
