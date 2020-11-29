from tree_search import *
from math import hypot
from mapa import Map
from consts import Tiles, TILES
import itertools
import copy

def minimal_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return hypot(x1-x2, y1-y2)

def new_pos(pos, action):
    cx, cy = pos
    if   action == "w":
        return cx, cy - 1
    elif action == "a":
        return cx - 1, cy
    elif action == "s":
        return cx, cy + 1
    elif action == "d":
        return cx + 1, cy

def prior_pos(pos, action):
    cx, cy = pos
    if   action == "w":
        return cx, cy + 1
    elif action == "a":
        return cx + 1, cy
    elif action == "s":
        return cx, cy - 1
    elif action == "d":
        return cx - 1, cy

class SokobanDomain(SearchDomain):
    def __init__(self, filename):
        self.change_map(filename)

    def change_map(self, filename):
        self.level = filename
        self.map = Map(filename)
        self.map.clear_tile(self.map.keeper)
        for box in self.map.boxes:
            self.map.clear_tile(box)

    def is_blocked(self, other_boxes, pos):
        return self.map.is_blocked(pos) or pos in other_boxes

    def is_blocked_2(self, pos1, pos2):
        return (self.map.is_blocked(pos1)) and (self.map.is_blocked(pos2))

    def trapped(self, boxes):
        for box in boxes:
            if box in self.map.empty_goals:
                continue
            pos1= new_pos(box, "a")
            pos2= new_pos(box, "w")
            pos3= new_pos(box, "d")
            pos4= new_pos(box, "s")
            if self.is_blocked_2(pos1, pos2) or self.is_blocked_2(pos3, pos4) or  self.is_blocked_2(pos3, pos2) or self.is_blocked_2(pos1, pos4):
                return True
        return False

    def sort(self, boxes):
        return sorted(boxes, key=lambda pos: (pos[0], pos[1]))

    def get_newboxes(self, boxes, box, direction):
        newboxes = copy.deepcopy(boxes)
        newboxes[boxes.index(box)] = new_pos(box, direction)
        return newboxes

    def get_other_boxes(self, boxes, box_goal):
        boxes2 = copy.deepcopy(boxes)
        boxes2.remove(box_goal)
        return boxes2


    def actions(self,state):
        boxes = state["boxes"]
        player = state["player"]
        actlist = []
        for box in boxes:
            other_boxes = self.get_other_boxes(boxes, box)
            for direction in [direction for direction in ["w","a","s","d"] if not (self.is_blocked(other_boxes, new_pos(box, direction)) or self.trapped(self.get_newboxes(boxes, box, direction)))]:
                new_tree = SearchTree(SearchProblem(PlayerDomain(self.level, boxes), player, prior_pos(box, direction)), 'a*')
                solution = new_tree.search()
                if(solution is not None):
                    path = new_tree.plan
                    print(new_tree.problem.domain.map)
                    print("\n", box)
                    print("\n", path)
                    actlist += [(direction, box, path)]
        return actlist

    def result(self,state,action):
        direction, box, path = action
        return {"boxes": self.get_newboxes(state["boxes"], box, direction), "player": box}
        
        
    def cost(self, state, action):
        return 1

    #https://www.kite.com/python/answers/how-to-get-all-unique-combinations-of-two-lists-in-python
    def heuristic(self, state, goal):
        return 0
        #return ([sum([minimal_distance(comb[0], comb[1]) for pair in comb]) for comb in [list(zip(each_permutation, goal)) for each_permutation in itertools.permutations(state, len(goal))]].sort(key= lambda x: int(x), Reverse=True))[0]

    def equivalent(self,state1,state2):
        return (self.sort(state1["boxes"])==self.sort(state2["boxes"])) and state1["player"]==state2["player"]

    def satisfies(self, state, goal):
        return (self.sort(state["boxes"])==self.sort(goal["boxes"]))








class PlayerDomain(SearchDomain):
    def __init__(self, filename, boxes):
        self.boxes = boxes
        self.change_map(filename, boxes)

    def change_map(self, filename, boxes):
        self.level = filename
        self.map = Map(filename)
        self.map.clear_tile(self.map.keeper)
        for box in self.map.boxes:
            self.map.clear_tile(box)
        for goal in self.map.empty_goals:
            (x, y) = goal
            self.map._map[y][x] = Tiles.FLOOR
        for box in boxes:
            self.map.set_tile(box, Tiles.WALL)

    def actions(self,state):
        return [direction for direction in ["w","a","s","d"] if not self.map.is_blocked(new_pos(state, direction))]

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