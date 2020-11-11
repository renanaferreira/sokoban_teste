from tree_search import *
from math import hypot
from mapa import Map
from consts import Tiles, TILES

def minimal_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return hypot(x1-x2, y1-y2)


class SokobanDomain(SearchDomain):
    def __init__(self, filename):
        self.change_map(filename)

    
    def toggle_map(self, state=None):
        if(state != None):
            self.fill_map(self, state)
        else:
            self.emptyMap()


    def fill_map(self, state):
        for box in state["boxes"]:
            self.map.set_tile(box, Tiles.BOX)
        self.map.set_tile(state["player"], Tiles.MAN)

    def empty_map(self):
        self.map.clear_tile(self.map.keeper)
        boxs = self.map.boxes
        for box in boxs:
            self.map.clear_tile(box)

    def change_map(self, filename):
        self.level = filename
        self.map = Map(filename)
        self.states = []
        self.is_empty = False
        self.toogle_map()

    def actions(self,state):
        self.toggle_map(state)
        actions = []
        for direction in ["w","a","s","d"]:
            if(self.can_move(self.map.keeper, direction)): 
                actions += [direction]
        self.toggle_map()
        return actions

    def can_move(self, cur, direction):
        """Move an entity in the game."""
        assert direction in "wasd", f"Can't move in {direction} direction"

        cx, cy = cur
        ctile = self.map.get_tile(cur)

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
        if self.map.is_blocked(npos):
            return False
        if self.map.get_tile(npos) in [Tiles.BOX,Tiles.BOX_ON_GOAL,]:  # next position has a box?
            if ctile & Tiles.MAN == Tiles.MAN:  # if you are the keeper you can push
                if not self.move(npos, direction):  # as long as the pushed box can move
                    return False
            else:  # you are not the Keeper, so no pushing
                return False
        
        return True

    def move(self, cur, direction):
        """Move an entity in the game."""
        assert direction in "wasd", f"Can't move in {direction} direction"

        cx, cy = cur
        ctile = self.map.get_tile(cur)

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
        if self.map.is_blocked(npos):
            return False
        if self.map.get_tile(npos) in [Tiles.BOX,Tiles.BOX_ON_GOAL,]:  # next position has a box?
            if ctile & Tiles.MAN == Tiles.MAN:  # if you are the keeper you can push
                if not self.move(npos, direction):  # as long as the pushed box can move
                    return False
            else:  # you are not the Keeper, so no pushing
                return False

        # actually update map
        self.map.set_tile(npos, ctile)
        self.map.clear_tile(cur)
        
        return True

    def result(self,state,action):
        goal = self.map.empty_goals
        self.toggle_map(state)
        self.move(self.map.keeper, action)
        newstate = {}
        newstate["player"] = self.map.keeper
        newstate["boxes"]  = self.map.boxes
        self.toggle_map()
        if(self.trapped(newstate, goal)):
            return None
        return newstate
        

    def cost(self, state, action):
        return 1

    def heuristic(self, state, goal): 
        sum = 0
        list1 = state["boxes"]
        list2 = goal["boxes"]
        for i in range(len(list1)):
            sum += minimal_distance(list1[i],list2[i])
        return sum


    def satisfies(self, state, goal):
        self.toggle_map(state)
        return self.map.completed
    
    def goal_box(self, box, goal):
        if box in goal["boxes"]:
            return True
        return False

    def trapped(self, state, goal):
        for box in state["boxes"]:
            if self.goal_box(x, goal):
                continue
            (x, y) = box

            pos_m_n=(x-1, y)
            pos_n_m=(x, y-1)
            if self.map.is_blocked(pos_m_n) and self.map.is_blocked(pos_n_m):
                return True

            pos_p_n=(x+1, y)
            pos_n_p=(x, y+1)
            if self.map.is_blocked(pos_p_n) and self.map.is_blocked(pos_n_p):
                return True

            pos_p_n=(x+1, y)
            pos_n_m=(x, y-1)
            if self.map.is_blocked(pos_p_n) and self.map.is_blocked(pos_n_m):
                return True

            pos_m_n=(x-1, y)
            pos_n_p=(x, y+1)
            if self.map.is_blocked(pos_m_n) and self.map.is_blocked(pos_n_p):
                return True
        
        return False
