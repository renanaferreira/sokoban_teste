from tree_search import *
from math import hypot

#state = {"player": (x, y),"boxes": [(x, y),...]}
#assert len(state["goals"]) == len(state["boxes"])
#action = "WASD"
class SokobanDomain(SearchDomain):
    def __init__(self, map):
        self.map = map

    def actions(self,state):
        #precisa evitar situações de deadlock
        actlist = []
        (player_x, player_y) = state["player"]
        #right
        if (player_x + 1, player_y) is in state["boxes"]:
            actlist.append("d")
        #left
        if (player_x - 1, player_y) is in state["boxes"]:
            actlist.append("d")
        if self.map
        return actlist 

    def result(self,state,action):
        #precisa modificar o valor de boxes e player
        (C1,C2) = action
        if C1==city:
            return C2

    def cost(self, state, action):
        #será que pode se dizer que sempre retorna 1?
        return 1

    def heuristic(self, state, goal):
        #Precisa procurar a menor heuristica por box-goal pair, e cada caixa só pode parear com
        #goal
        #minha ideia é encontrar a "combinação" cuja soma das heuristicas seja a menor possivel
        # será que é preciso analisar cada combinação? 
        x1,y1 = self.coordinates[city]
        x2,y2 = self.coordinates[goal_city]
        return hypot(x1-x2, y1-y2)

    def satisfies(self, state, goal):
    #Precisa garantir que cada box_position equivala a uma goal_position, e apenas uma
        boxes = state["boxes"]
        for box 
        return 