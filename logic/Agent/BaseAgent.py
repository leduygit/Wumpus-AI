import random
from pysat.solvers import Glucose3
from pysat.formula import CNF

DIRECTION = ['U', 'R', 'D', 'L']

ACTION = ['Foward', 'Turn Left', 'Turn Right', 'Heal']
# F: move forward
# TL: turn left
# TR: turn right
# H: Heal

def wumpus(x, y):
    return 16 * x + 4 * y + 1

def breeze(x, y):
    return 16 * x + 4 * y + 2

def stench(x, y):
    return 16 * x + 4 * y + 3

def agent(x, y, d):
    # d: 0=N, 1=E, 2=S, 3=W
    return 16 * x + 4 * y + d + 4

def pit(x, y):
    return 16 * x + 4 * y + 8

def shoot(d):
    # d: 0=N, 1=E, 2=S, 3=W
    return 64 + d + 1


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
        self.model = Glucose3()
        self.kb = CNF()

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

    def add_percept(self, position, percept):
        i, j = position
        print(percept)
        if (type(percept) == str):
            percept = [percept]

        for p in percept:
            if p == 'S':
                self.percept_stench(position)
            elif p == 'B':
                self.percept_breeze(position)
            elif (p not in self.grid[i][j]):
                self.grid[i][j].append(p)

    def get_neighbors(self, i, j):
        neighbors = []
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in direction:
            x, y = i + d[0], j + d[1]
            if self.is_valid_move(x, y):
                neighbors.append((x, y))
        return neighbors

    def percept_stench(self, position):
        self.kb.append([-stench(position)])
        i, j = position
        neighbors = self.get_neighbors(i, j)
        for n in neighbors:
            self.kb.append([wumpus(n[0], n[1])])

    def percept_breeze(self, position):
        self.kb.append([-breeze(position)])
        i, j = position
        neighbors = self.get_neighbors(i, j)
        for n in neighbors:
            self.kb.append([pit(n[0], n[1])])

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

    def make_action(self):
        # return random action
        # input the action to the environment

        solver = Glucose3()
        solver.append_formula(self.kb)
        if self.direction == 'U':
            if not self.is_valid_move(self.position[0] - 1, self.position[1]):
                return 'Turn Right'
            print(solver.solve(assumptions=[wumpus(self.position[0] - 1, self.position[1])]))
            if solver.solve(assumptions=[wumpus(self.position[0] - 1, self.position[1])]) == False:
                return 'Shoot'
            if solver.solve(assumptions=[pit(self.position[0] - 1, self.position[1])]) == False:
                return 'Forward'
        elif self.direction == 'R':
            if not self.is_valid_move(self.position[0], self.position[1] + 1):
                return 'Turn Right'
            print(solver.solve(assumptions=[pit(self.position[0], self.position[1] + 1)]))
            if solver.solve(assumptions=[wumpus(self.position[0], self.position[1] + 1)]) == False:
                return 'Shoot'
            if solver.solve(assumptions=[pit(self.position[0], self.position[1] + 1)]) == True:
                return 'Forward'
        elif self.direction == 'D':
            if not self.is_valid_move(self.position[0] + 1, self.position[1]):
                return 'Turn Right'
            if solver.solve(assumptions=[wumpus(self.position[0] + 1, self.position[1])]) == False:
                return 'Shoot'
            if solver.solve(assumptions=[pit(self.position[0] + 1, self.position[1])]) == False:
                return 'Forward'
        elif self.direction == 'L':
            if not self.is_valid_move(self.position[0], self.position[1] - 1):
                return 'Turn Right'
            if solver.solve(assumptions=[wumpus(self.position[0], self.position[1] - 1)]) == False:
                return 'Shoot'
            if solver.solve(assumptions=[pit(self.position[0], self.position[1] - 1)]) == False:
                return 'Forward'

        solver.delete()
        return 'Turn Right'
        # clear the screen
        print('\n' * 100)
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
