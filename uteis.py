import copy
from math import hypot

#retorna a nova posição a partir de certa ação
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

#retorna a posição anterior a certa ação
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

#retorna a posicao em medida legivel a users(para logging purposes)
def readable_pos(pos):
    x, y = pos
    return x+1,y+1

#retorna a distancia teoricamente minima entre duas posicoes
def minimal_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return hypot(x1-x2, y1-y2)

def get_newboxes(boxes, box, direction):
    return get_other_boxes(boxes, box) + [new_pos(box, direction)]

def get_other_boxes(boxes, box):
    other_boxes = copy.deepcopy(boxes)
    other_boxes.remove(box)
    return other_boxes

def sort_boxes(boxes):
    return sorted(boxes, key=lambda pos: (pos[0], pos[1]))
