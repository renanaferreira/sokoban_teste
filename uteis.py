import copy
from math import hypot

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

def get_newboxes(boxes, box, direction):
    newboxes = copy.deepcopy(boxes)
    newboxes[boxes.index(box)] = new_pos(box, direction)
    return newboxes

def get_other_boxes(boxes, box_goal):
    boxes2 = copy.deepcopy(boxes)
    boxes2.remove(box_goal)
    return boxes2

def readable_pos(pos):
    x, y = pos
    return x+1,y+1
