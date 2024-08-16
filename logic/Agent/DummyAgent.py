from logic.Agent.BaseAgent import BaseAgent
from logic.Agent.BaseAgent import wumpus, breeze, stench, pit, poison_gas, whiff, healing_potion, glow
from collections import deque

DIRECTION = ['U', 'R', 'D', 'L']
FORWARD = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class DummyAgent(BaseAgent):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.safe_cells = [[None for _ in range(width)] for _ in range(height)] 
        self.width = width
        self.height = height
        

    def is_safe(self, position):
        i, j = position

        is_wumpus = self.solve_assumption([wumpus(i, j)])
        is_pit = self.solve_assumption([pit(i, j)])
        is_poison_gas = self.solve_assumption([poison_gas(i, j)])

        if is_wumpus == True:
            return False
        
        if is_pit == True:
            return False
        
        if is_poison_gas == True and self.get_health() <= 25:
            return False

        if is_poison_gas == True and self.get_health() > 25:
            return True

        if is_wumpus == False and is_pit == False:
            return True
        
        return None

    def add_safe_cell(self):
        for i in range(self.height):
            for j in range(self.width):
                if not self.safe_cells[i][j]:
                    self.safe_cells[i][j] = self.is_safe((i, j))
                

    def bfs_to_nearest_safe(self):
        visited = [[[False for _ in range(self.width)] for _ in range(self.height)] for _ in range(4)]



        queue = deque([(self.get_position(), self.get_direction(), [])])

        # queue with sequence of actions

        # action = 'Foward', 'Turn Left', 'Turn Right'

        action = ['Forward', 'Turn Left', 'Turn Right']



        while queue:
            position, direction, action_sequence = queue.popleft()

            i, j = position

            if self.safe_cells[i][j] != True:
                continue

            if self.safe_cells[i][j] == True and not self.visited[i][j]:
                print("Safe Cell: ", i, j)
                print(self.visited[i][j])
                return action_sequence
            
            if visited[i][j][DIRECTION.index(direction)]:
                continue

            visited[i][j][DIRECTION.index(direction)] = True

            for a in action:
                direction_index = DIRECTION.index(direction)

                if a == 'Forward':
                    new_position = (i + FORWARD[direction_index][0], j + FORWARD[direction_index][1])
                    if self.is_valid_move(new_position[0], new_position[1]):
                        queue.append((new_position, direction, action_sequence + ['Forward']))
                
                elif a == 'Turn Left':
                    new_direction = DIRECTION[(direction_index - 1) + 4 % 4]
                    queue.append((position, new_direction, action_sequence + ['Turn Left']))

                elif a == 'Turn Right':
                    new_direction = DIRECTION[(direction_index + 1) % 4]
                    queue.append((position, new_direction, action_sequence + ['Turn Right']))

        return []
    
    def bfs_to_start(self):
        visited = [[[False for _ in range(self.width)] for _ in range(self.height)] for _ in range(4)]

        queue = deque([(self.get_position(), self.get_direction(), [])])

        action = ['Forward', 'Turn Left', 'Turn Right']

        while queue:
            position, direction, action_sequence = queue.popleft()

            i, j = position

            if i == self.height - 1 and j == 0:
                return action_sequence

            if visited[i][j][DIRECTION.index(direction)]:
                continue

            visited[i][j][DIRECTION.index(direction)] = True

            for a in action:
                direction_index = DIRECTION.index(direction)

                if a == 'Forward':
                    new_position = (i + FORWARD[direction_index][0], j + FORWARD[direction_index][1])
                    if self.is_valid_move(new_position[0], new_position[1]):
                        queue.append((new_position, direction, action_sequence + ['Forward']))
                
                elif a == 'Turn Left':
                    new_direction = DIRECTION[(direction_index - 1) + 4 % 4]
                    queue.append((position, new_direction, action_sequence + ['Turn Left']))

                elif a == 'Turn Right':
                    new_direction = DIRECTION[(direction_index + 1) % 4]
                    queue.append((position, new_direction, action_sequence + ['Turn Right']))

        return []


    def return_to_start(self):
        if self.get_position() == (self.height - 1, 0):
            return "Climb"
        
        self.action_sequence = self.bfs_to_start()

        
        if self.action_sequence:
            action = self.action_sequence.pop(0)
            return action

    def make_action(self):

        current_percept = self.get_percept(self.get_position())

        if 'G' in current_percept:
            return "Grab"
        
        if 'H_P' in current_percept:
            return "Grab"

        # if there is no None inn safe cell --> go back to the start
        if not any(None in row for row in self.safe_cells):
            return self.return_to_start()


        self.add_safe_cell()

        self.action_sequence = self.bfs_to_nearest_safe()

        print("Action Sequence: ", self.action_sequence)

        print("Current Position: ", self.get_position())
        print("Current Direction: ", self.get_direction())
        for i in range(self.height):
            for j in range(self.width):
                print(self.safe_cells[i][j], end=' ')
            print()

        if self.action_sequence:
            action = self.action_sequence.pop(0)
            return action
        

        # print safe cells

        print("Visited:")
        for i in range(self.height):
            for j in range(self.width):
                print(self.visited[i][j], end=' ')
            print()

        print("Grid:")
        for i in range(self.height):
            for j in range(self.width):
                print(self.grid[i][j], end=' ')
            print()

        
        if self.get_health() < 50:
            return "Heal"
        
            
        if 'S' in current_percept:
            direction = self.get_direction()
            i, j = self.get_position()

            index = DIRECTION.index(direction)
            u, v = i + FORWARD[index][0], j + FORWARD[index][1]

            if self.safe_cells[u][v] != True:
                return "Shoot"
            else:
                return "Turn Left"
            
        # no action to take then return to the start
            
        return self.return_to_start()
            
        
            
        
