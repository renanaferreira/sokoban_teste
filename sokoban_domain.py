from tree_search import *
from math import hypot
from mapa import Map
from consts import Tiles, TILES
from copy import deepcopy

def minimal_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return hypot(x1-x2, y1-y2)

def new_pos(self, pos, action):
    cx, cy = pos
    if action == "w":
        return cx, cy - 1
    elif action == "a":
        return cx - 1, cy
    elif action == "s":
        return cx, cy + 1
    elif action == "d":
        return cx + 1, cy

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

    def is_blocked(self, pos1, pos2):
        return self.map.is_blocked(pos1) and self.map.is_blocked(pos2)

    def trapped(self, boxes):
        for box in boxes:
            if box in self.map.empty_goals:
                continue
            (x, y) = box

            pos1=(x-1, y)
            pos2=(x, y-1)
            pos3=(x+1, y)
            pos4=(x, y+1)
            if self.is_blocked(pos1, pos2) or self.is_blocked(pos3, pos4) or  self.is_blocked(pos3, pos2) or self.is_blocked(pos1, pos4):
                return True
        return False

    def sort(self, boxes):
        return sorted(boxes, key=lambda pos: (pos[0], pos[1]))

    def actions(self,state):
        boxes = state["boxes"]
        actlist = []
        for box in boxes:
            for direction in [direction for direction in ["w","a","s","d"] if self.map.is_blocked(new_pos(box, direction))]:
                newboxes = state
                newboxes.replace(box, new_pos(box, direction))
                if(self.trapped(newboxes)):
                    continue
                solution = SearchTree(SearchProblem(PlayerDomain(self.level, newboxes), state["player"], box), self.strategy).search()
                if(solution is not None):
                    actlist += (direction, box, solution)
        return actlist

    def result(self,state,action):
        direction, box, solution = action
        state["boxes"].replace(box, new_pos(box, direction))
        state["player"] = box
        return state
        
    def cost(self, state, action):
        return 1

    def heuristic(self, state, goal): 
        return 0

    def equivalent(self,state1,state2):
        return self.sort(state1)==self.sort(state2)

    def satisfies(self, state, goal):
        return self.equivalent(state, goal)


class PlayerDomain(SearchDomain):
    def __init__(self, filename, boxes):
        self.change_map(filename, boxes)

    def change_map(self, filename, boxes):
        self.level = filename
        self.map = Map(filename)
        self.map.clear_tile(self.map.keeper)
        for box in self.map.boxes:
            self.map.clear_tile(box)
        for goal in self.map.empty_goals:
            self.map.set_tile(goal, Tiles.FLOOR)
        for box in boxes:
            self.map.set_tile(box, Tiles.WALL)

    def actions(self,state):
        return [direction for direction in ["w","a","s","d"] if self.map.is_blocked(new_pos(state, direction))]

    def result(self,state,action):
        return new_pos(state, action)
        
    def cost(self, state, action):
        return 1

    def heuristic(self, state, goal): 
        return minimal_distance(state, goal)

    def equivalent(self,state1,state2):
        return state1==state2

    def satisfies(self, state, goal):
        return self.equivalent(state, goal)