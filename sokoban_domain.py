from tree_search import *
from math import hypot
from mapa import Map
from consts import Tiles, TILES

def minimal_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return hypot(x1-x2, y1-y2)

#state = 
#action = "WASD"
class SokobanDomain(SearchDomain):
    def __init__(self, filename):
        self.level = filename
        self.map = Map(filename)
        self.states = []
        self.emptyMap()   

    def fillMap(self, state):
        for box in state["boxes"]:
            self.map.set_tile(box, Tiles.BOX)
        self.map.set_tile(state["player"], Tiles.MAN)

    def emptyMap(self):
        self.map.clear_tile(self.map.keeper)
        boxs = self.map.boxes
        for box in boxs:
            self.map.clear_tile(box)


    def actions(self,state):
        self.fillMap(state)
        actions = []
        for direction in ["w","a","s","d"]:
            if(self.can_move(self.map.keeper, direction)): 
                actions += [direction]
        self.emptyMap()
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
        self.fillMap(state)
        self.move(self.map.keeper, action)
        newstate = {}
        newstate["player"] = self.map.keeper
        newstate["boxes"]  = self.map.boxes
        self.emptyMap()
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
        self.fillMap(state)
        return self.map.completed
    
    def satisfies_box(self, box, goal):
        boxes=goal["boxes"];
        if box in boxes:
            return True
        return False