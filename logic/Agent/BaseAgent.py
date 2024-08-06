import random

DIRECTION = ['U', 'R', 'D', 'L']

ACTION = ['F', 'TL', 'TR']
# F: move forward
# TL: turn left
# TR: turn right


class BaseAgent:
    def __init__(self, width, height):
        # bottom left corner
        self.position = (height - 1, 0)
        self.direction = 'R'
        self.grid = [['' for _ in range(width)] for _ in range(height)]

    def add_percept(self, percept):
        i, j = self.position
        self.grid[i][j] = percept

    def get_position(self):
        return self.position
    
    def get_direction(self):
        return self.direction
    
    def is_valid_move(self, i, j):
        if 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0]):
            return True
        return False
    
    def update_state(self, action):
        if action == 'F':
            # update position
            i, j = self.position
            dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            id = DIRECTION.index(self.direction)
            if self.is_valid_move(i + dir[id][0], j + dir[id][1]):
                self.position = (i + dir[id][0], j + dir[id][1])
        
        elif action == 'TL':
            id = DIRECTION.index(self.direction)
            self.direction = DIRECTION[(id - 1 + id) % 4]
        
        elif action == 'TR':
            id = DIRECTION.index(self.direction)
            self.direction = DIRECTION[(id + 1) % 4]

    def make_action(self):
        # return random action
        action = ACTION[random.randint(0, 2)]
        self.update_state(action)
        return action

