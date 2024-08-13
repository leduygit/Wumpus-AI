import random
import pysat
from pysat.solvers import Glucose3
from pysat.formula import CNF
import pysat.solvers

DIRECTION = ['U', 'R', 'D', 'L']

ACTION = ['Foward', 'Turn Left', 'Turn Right', 'Heal', 'Shoot']
# F: move forward
# TL: turn left
# TR: turn right
# H: Heal

CELL = ['W', 'P', 'P_G', 'H_P', 'B', 'S', 'W_H', 'G_L']

DANGER = ['W', 'P', 'P_G']

EFFECT = ['W_H', 'G_L', "B", 'S']

ACTION_EFFECT = {
    'W_H': 'P_G',
    'G_L': 'H_P',
    'B': 'P',
    'S': 'W',
}

def wumpus(x, y):
    if (x == 0 and y == 0):
        return 6969
    return 10 * x + y 

def breeze(x, y):
    return 100 + 10 * x + y

def stench(x, y):
    return 200 + 10 * x + y

# def agent(x, y, d):
#     # d: 0=N, 1=E, 2=S, 3=W
#     return 303 + 10 * x + y + d

def pit(x, y):
    return 300 + 10 * x + y

# def shoot(d):
#     # d: 0=N, 1=E, 2=S, 3=W
#     return 64 + d + 1

# def safe(x, y):
#     return 400 + 10 * x + y

def poison_gas(x, y):
    return 500 + 10 * x + y

def whiff(x, y):
    return 600 + 10 * x + y

def healing_potion(x, y):
    return 700 + 10 * x + y

def glow(x, y):
    return 800 + 10 * x + y

class BaseAgent:
    def __init__(self, width, height):
        # bottom left corner
        self.position = (height - 1, 0)
        self.direction = 'R'
        self.grid = [[[] for _ in range(width)] for _ in range(height)]
        self.health = 100
        self.score = 0
        self.potion = 0
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.kb = CNF()
        # self.kb.append([safe(height - 1, 0)])

        self.Percept_to_Function = {
            'W': wumpus,
            'P': pit,
            'P_G': poison_gas,
            'H_P': healing_potion,
            'B': breeze,
            'S': stench,
            'W_H': whiff,
            'G_L': glow
        }

        # add agent to the grid
        i, j = self.position
        self.grid[i][j].append('A')

    def print_agent_info(self):
        print('Position: ', self.position)
        print('Direction: ', self.direction)
        print('Health: ', self.health)
        print('Score: ', self.score)
        print('Potion: ', self.potion)

        #print grid

        self.print_grid()
        print('-' * 20)

    def print_grid(self):
        for row in self.grid:
            print(row)


    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def get_potion(self):
        return self.potion

    def set_potion(self, potion):
        self.potion = potion

    def remove_percept(self, position, percept):
        i, j = position
        if (type(percept) == str):
            percept = [percept]

        for p in percept:
            if (p in self.grid[i][j]):
                self.grid[i][j].remove(p)

    def set_visited(self, position):
        i, j = position
        self.visited[i][j] = True

    def get_visited(self, position):
        i, j = position
        return self.visited[i][j]
    
    def simplify(self):
        # simplify the knowledge base
        new_kb = CNF()
        for clause in self.kb:
            if len(clause) == 1:
                new_kb.append(clause)
        
        for clause in self.kb:
            if len(clause) > 1:
                new_clause = []
                for c in clause:
                    if -c not in self.kb:
                        new_clause.append(c)
        
        self.kb = new_kb

    def add_percept(self, position, percept):
        self.simplify()
        i, j = position
        print("Current Percept: ", percept)
        if (type(percept) == str):
            percept = [percept]

        for p in percept:
            if p == 'S':
                self.percept_stench(position)
            if p == 'B':
                self.percept_breeze(position)
            if p == 'W_H':
                self.percept_whiff(position)
            if p == 'G_L':
                self.percept_glow(position)
            if (p not in self.grid[i][j]):
                self.grid[i][j].append(p)



        if 'Sc' in percept:
            # add -wumpus(i, j) to the knowledge base
            
            if (wumpus(i, j) in self.kb):
                self.kb.remove(wumpus(i, j))

            self.kb.append([-wumpus(i, j)])
            return

        # update knowledge base
        for c in CELL:
            if c not in percept:
                self.kb.append([-self.Percept_to_Function[c](i, j)])

        # update neighbors
        neighbors = self.get_neighbors(i, j)
        for e in EFFECT:
            if e not in percept:
                for n in neighbors:
                    a = ACTION_EFFECT[e]
                    self.kb.append([-self.Percept_to_Function[a](n[0], n[1])])

    def get_neighbors(self, i, j):
        neighbors = []
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in direction:
            x, y = i + d[0], j + d[1]
            if self.is_valid_move(x, y):
                neighbors.append((x, y))
        return neighbors

    def percept_stench(self, position):
        # self.kb.append([-stench(position[0], position[1])])
        i, j = position
        neighbors = self.get_neighbors(i, j)
        _ = []
        for n in neighbors:
            _.append(wumpus(n[0], n[1]))
        if (position == (1, 3)):
            print("Stench: ", _)
        self.kb.append(_)

    def percept_breeze(self, position):
        # self.kb.append([-breeze(position[0], position[1])])
        i, j = position
        neighbors = self.get_neighbors(i, j)
        _ = []
        for n in neighbors:
            _.append(pit(n[0], n[1]))
        self.kb.append(_)

    def percept_whiff(self, position):
        i, j = position
        neighbors = self.get_neighbors(i, j)
        _ = []
        for n in neighbors:
            _.append(poison_gas(n[0], n[1]))
        self.kb.append(_)

    def percept_glow(self, position):
        i, j = position
        neighbors = self.get_neighbors(i, j)
        _ = []
        for n in neighbors:
            _.append(healing_potion(n[0], n[1]))
        self.kb.append(_)

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction

    def set_position(self, position):
        # remove 'A' from the previous position
        i, j = self.position
        self.grid[i][j].remove('A')
        self.position = position
        i, j = self.position
        self.grid[i][j].append('A')

    def set_direction(self, direction):
        self.direction = direction

    def is_valid_move(self, i, j):
        if 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0]):
            return True
        return False

    def solve_assumption(self, assumption, solver):
        model = solver.solve(assumptions=assumption)
        if model:
            return solver.get_model()
        return []

    def make_action(self):
        # return random action
        # input the action to the environment

        print(f"Clauses : {self.kb.clauses}")
        solver = pysat.solvers.Solver(name='glucose3', bootstrap_with=self.kb.clauses)
        self.kb.clauses.append([1000])
        print("current position: ", self.position)
        for neighbor in self.get_neighbors(self.position[0], self.position[1]):
            print(self.kb.clauses)
            print("neighbor: ", neighbor)
            model_positive = self.solve_assumption([wumpus(neighbor[0], neighbor[1])], solver)
            model_negative = self.solve_assumption([-wumpus(neighbor[0], neighbor[1])], solver)
            # print(f"Model: {len(model)}")
            result = None
            if len(model_positive) == 0:
                result = False
            if len(model_negative) == 0:
                result = True
            # if both are empty, then
            if len(model_positive) == 0 and len(model_negative) == 0:
                result = None
            print("percept for wumpus: ", result)
        #     print("percept for pit: ", model[pit(neighbor[0], neighbor[1])])
        #     print("percept for safe: ", model[safe(neighbor[0], neighbor[1])])
        solver.delete()
        print('Choices:')
        print('1. Forward')
        print('2. Turn Left')
        print('3. Turn Right')
        print('4. Heal')
        print('5. Shoot')
        print('6. Climb')
        print('7. Grab')
        print()

        print('Agent info:')
        self.print_agent_info()


        action = input('Enter action: ')
        if action == '1':
            return 'Forward'
        elif action == '2':
            return 'Turn Left'
        elif action == '3':
            return 'Turn Right'
        elif action == '4':
            return 'Heal'
        elif action == '5':
            return 'Shoot'
        elif action == '6':
            return 'Climb'
        elif action == '7':
            return 'Grab'
        else:
            raise ValueError('Invalid action')
        return action
