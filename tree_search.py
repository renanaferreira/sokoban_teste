
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod
import random

def compareStates(state01, state02):
    if(state01["player"] != state02["player"]):
        return False
    for box in state01["boxes"]:
        if box not in state02["boxes"]:
            return False
    for box in state02["boxes"]:
        if box not in state01["boxes"]:
            return False
    return True

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
        
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

    def goal_box(self, box):
        return self.domain.satisfies_box(box, self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, depth, cost, heuristic=0, action=None): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action

    
    def in_parent(self, state):
        if self.parent == None:
            return False
        into = (compareStates(state, self.parent.state)) or (self.parent.in_parent(state))
        return into

    def __str__(self):
        return f"no({str(self.state)},{str(self.depth)}, {str(self.action)})"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth', mapp=None): 
        self.problem = problem
        root = SearchNode(problem.initial, None, 0, 0, self.problem.domain.heuristic(
            self.problem.initial, self.problem.goal))
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 1
        self.non_terminals = 0
        self.avg_ramification = None
        self.map=mapp

    @property
    def length(self):
        if self.solution:
            return self.solution.depth
        return None

    @property
    def cost(self):
        if self.solution:
            return self.solution.cost
        return None
    
    @property
    def plan(self):
        if self.solution:
            return self.get_plan(self.solution)
        return None

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    def get_plan(self,node):
        if node.parent == None:
            return []
        plan = self.get_plan(node.parent)
        plan += [node.action]
        return plan

    # procurar a solucao
    def search(self, limit=None):
        count = 0
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            print(count); count += 1
            self.non_terminals+=1
            self.terminals=len(self.open_nodes)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.avg_ramification = (self.terminals+self.non_terminals-1)/self.non_terminals
                return self.get_path(node)
            lnewnodes = []

            shuffleActions = self.problem.domain.actions(node.state)
            random.shuffle(shuffleActions)
            for a in shuffleActions:
                # newstate = posição das caixas
                newstate = self.problem.domain.result(node.state,a)
                if newstate == None:
                    continue
                
                newnode = SearchNode(newstate,node, node.depth+1, node.cost+self.problem.domain.cost(node.state, a),
                                             self.problem.domain.heuristic(newstate,self.problem.goal), a)
                if not node.in_parent(newstate) and (limit is None or newnode.depth <= limit):
                    lnewnodes.append(newnode)        
            self.add_to_open(lnewnodes)

        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key = lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key = lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key = lambda node: node.heuristic + node.cost)

    def encurralado(self, boxes):
        for x in boxes:
            if self.problem.goal_box(x):
                continue
            caixa_x = x[0]
            caixa_y = x[1]

            pos_m_n=(caixa_x-1, caixa_y)
            pos_n_m=(caixa_x, caixa_y-1)

            pos_p_n=(caixa_x+1, caixa_y)
            pos_n_p=(caixa_x, caixa_y+1)

            pos_p_n=(caixa_x+1, caixa_y)
            pos_n_m=(caixa_x, caixa_y-1)

            pos_m_n=(caixa_x-1, caixa_y)
            pos_n_p=(caixa_x, caixa_y+1)

            if self.map.is_blocked(pos_m_n) and self.map.is_blocked(pos_n_m):
                return True

            if self.map.is_blocked(pos_p_n) and self.map.is_blocked(pos_n_p):
                return True

            if self.map.is_blocked(pos_p_n) and self.map.is_blocked(pos_n_m):
                return True

            if self.map.is_blocked(pos_m_n) and self.map.is_blocked(pos_n_p):
                return True
        
        return False

            
