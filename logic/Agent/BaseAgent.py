import pysat
from pysat.solvers import Glucose3
from pysat.formula import CNF
import pysat.solvers

def wumpus(x, y): return 6969 if (x == 0 and y == 0) else 10 * x + y
def breeze(x, y): return 100 + 10 * x + y
def stench(x, y): return 200 + 10 * x + y
def pit(x, y): return 300 + 10 * x + y
def poison_gas(x, y): return 500 + 10 * x + y
def whiff(x, y): return 600 + 10 * x + y
def healing_potion(x, y): return 700 + 10 * x + y
def glow(x, y): return 800 + 10 * x + y

ACTION = {
    '1': 'Forward',
    '2': 'Turn Left',
    '3': 'Turn Right',
    '4': 'Heal',
    '5': 'Shoot',
    '6': 'Climb',
    '7': 'Grab'
}

ACTION_EFFECT = {
    'W_H': 'P_G',
    'G_L': 'H_P',
    'B': 'P',
    'S': 'W',
}

PERCEPT_TO_LITERAL = {
    'S': wumpus,
    'B': pit,
    'W_H': poison_gas,
    'G_L': healing_potion
}


class BaseAgent:
    def __init__(self, width, height):
        self.position = (height - 1, 0)
        self.direction = 'U'
        self.grid = [[[] for _ in range(width)] for _ in range(height)]
        self.health = 100
        self.score = 0
        self.potion = 0
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.kb = CNF()
        self.is_wumpus = [[False for _ in range(width)] for _ in range(height)]

        self.PERCEPT_TO_FUNCTION = {
            'W': wumpus,
            'P': pit,
            'P_G': poison_gas,
            'H_P': healing_potion
        }

        i, j = self.position
        self.grid[i][j].append('A')

    def print_agent_info(self):
        print('Position: ', self.position)
        print('Direction: ', self.direction)
        print('Health: ', self.health)
        print('Score: ', self.score)
        print('Potion: ', self.potion)
        self.print_grid()
        print('-' * 20)

    def print_grid(self):
        for row in self.grid:
            print(row)

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = min(100, health)

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def get_potion(self):
        return self.potion

    def set_potion(self, potion):
        self.potion = potion

    def set_visited(self, position):
        i, j = position
        self.visited[i][j] = True

    def get_visited(self, position):
        i, j = position
        return self.visited[i][j]
    
    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction
    
    def get_percept(self, position):
        i, j = position
        return self.grid[i][j]

    def set_position(self, position):
        i, j = self.position
        self.grid[i][j].remove('A')
        self.position = position
        i, j = self.position
        self.grid[i][j].append('A')

    def set_direction(self, direction):
        self.direction = direction

    def get_is_wumpus(self, position):
        i, j = position
        return self.is_wumpus[i][j]
    
    def set_is_wumpus(self, position, is_wumpus):
        i, j = position
        self.is_wumpus[i][j] = is_wumpus

    def simplify(self):
        new_kb = CNF()
        for clause in self.kb.clauses:
            if len(clause) == 1 and clause not in new_kb:
                new_kb.append(clause)
        
        for clause in self.kb.clauses:
            if len(clause) > 1:
                new_clause = []
                for c in clause:
                    if [-c] not in self.kb.clauses:
                        new_clause.append(c)
                if new_clause not in new_kb and len(new_clause) > 0:
                    new_kb.append(new_clause)
        
        self.kb = new_kb


    def add_percept(self, position, percept):
        i, j = position
        print("Current Percept: ", percept)
        
        if isinstance(percept, str):
            percept = [percept]

        for p in percept:
            self.add_percept_to_kb(position, p)
            if p not in self.grid[i][j]:
                self.grid[i][j].append(p)

        if 'No-Sc' in percept:
            if [wumpus(i, j)] in self.kb.clauses:
                self.kb.clauses.remove([wumpus(i, j)])
            self.kb.append([-wumpus(i, j)])
            # self.kb.append([-pit(i, j)])  
            self.simplify()
            return

        if 'Sc' in percept:
            if [pit(i, j)] in self.kb.clauses:
                self.kb.clauses.remove([pit(i, j)])            
            self.kb.append([-pit(i, j)])
            self.simplify()
            return
        
        
        for c in self.PERCEPT_TO_FUNCTION.keys():
            if c not in percept:
                if [self.PERCEPT_TO_FUNCTION[c](i, j)] in self.kb.clauses:
                    self.kb.clauses.remove([self.PERCEPT_TO_FUNCTION[c](i, j)])
                self.kb.append([-self.PERCEPT_TO_FUNCTION[c](i, j)])

        neighbors = self.get_neighbors(i, j)
        for e in ACTION_EFFECT.keys():
            if e not in percept:
                for n in neighbors:
                    a = ACTION_EFFECT[e]
                    if [self.PERCEPT_TO_FUNCTION[a](n[0], n[1])] in self.kb.clauses:
                        self.kb.clauses.remove([self.PERCEPT_TO_FUNCTION[a](n[0], n[1])])
                    self.kb.append([-self.PERCEPT_TO_FUNCTION[a](n[0], n[1])])

        self.simplify()
    

    def remove_percept(self, position, percept):
        i, j = position
        if isinstance(percept, str):
            percept = [percept]

        for p in percept:
            if p in self.grid[i][j]:
                self.grid[i][j].remove(p)
                if p in self.PERCEPT_TO_FUNCTION:
                    clause = self.PERCEPT_TO_FUNCTION[p](i, j)
                    if [clause] in self.kb.clauses:
                        self.kb.clauses.remove([clause])


    def get_neighbors(self, i, j):
        neighbors = []
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in direction:
            x, y = i + d[0], j + d[1]
            if self.is_valid_move(x, y):
                neighbors.append((x, y))
        return neighbors
    
    def add_percept_to_kb(self, position, percept):
        i, j = position
        if percept in self.PERCEPT_TO_FUNCTION.keys():
            self.kb.append([self.PERCEPT_TO_FUNCTION[percept](i, j)])
            
        if percept not in PERCEPT_TO_LITERAL:
            return
        
        
        literal = PERCEPT_TO_LITERAL[percept]
        neighbors = self.get_neighbors(i, j)
        _ = []
        for n in neighbors:
            _.append(literal(n[0], n[1]))
        self.kb.append(_)

    def is_valid_move(self, i, j):
        return 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0])
    
    def solve_assumption(self, assumption):
        solver = pysat.solvers.Solver(name='glucose3', bootstrap_with=self.kb.clauses)
        positive_model = solver.solve(assumptions=assumption)
        negative_model = solver.solve(assumptions=[-a for a in assumption])

        # print("KB: ", self.kb.clauses)

        if not positive_model and not negative_model:
            raise ValueError('Invalid assumption')
        
        if not positive_model:
            solver.delete()
            return False
        if not negative_model:
            solver.delete()
            return True

        solver.delete()
        
        return None
    

    def make_action(self):
        print(f"Clauses : {self.kb.clauses}")
        print("current position: ", self.position)
        for neighbor in self.get_neighbors(self.position[0], self.position[1]):
            print(self.kb.clauses)
            print(f"Neighbor: {neighbor}")
            print(f"Wumpus: {self.solve_assumption([wumpus(neighbor[0], neighbor[1])])}")
            print(f"Pit: {self.solve_assumption([pit(neighbor[0], neighbor[1])])}")
            print(f"Poison Gas: {self.solve_assumption([poison_gas(neighbor[0], neighbor[1])])}")
            print(f"Healing Potion: {self.solve_assumption([healing_potion(neighbor[0], neighbor[1])])}")
        
        print('Choices:\n1. Forward\n2. Turn Left\n3. Turn Right\n4. Heal\n5. Shoot\n6. Climb\n7. Grab\n')

        self.print_agent_info()

        action = input('Enter action: ')
        if action in ACTION:
            return ACTION[action]
        else:
            raise ValueError('Invalid action')
