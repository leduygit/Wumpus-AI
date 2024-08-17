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
        
        if is_poison_gas == True and self.get_health() <= 50:
            return False

        if is_poison_gas == True and self.get_health() > 50:
            return True
        
        if is_pit == False and is_wumpus == False:
            return True
        
        
        return None

    def add_safe_cell(self):
        for i in range(self.height):
            for j in range(self.width):
                if not self.safe_cells[i][j]:
                    self.safe_cells[i][j] = self.is_safe((i, j))

        for i in range(self.height):
            for j in range(self.width):
                is_wumpus = self.solve_assumption([wumpus(i, j)])
                self.is_wumpus[i][j] = is_wumpus
                

    def bfs_to_nearest_safe(self):
        safe_cells = [(i, j) for i in range(self.height) for j in range(self.width) if self.safe_cells[i][j] and not self.visited[i][j]]

        return self.bfs_to_goal(safe_cells)

    def bfs_to_goal(self, goal):
        visited = [[[False for _ in range(self.width)] for _ in range(self.height)] for _ in range(4)]

        queue = deque([(self.get_position(), self.get_direction(), [])])

        action = ['Forward', 'Turn Left', 'Turn Right']

        while queue:
            position, direction, action_sequence = queue.popleft()

            i, j = position

            if not self.is_safe((i, j)) and (i, j) != self.get_position():
                continue

            if (i, j) in goal:
                return action_sequence

            if visited[DIRECTION.index(direction)][i][j]:
                continue

            visited[DIRECTION.index(direction)][i][j] = True

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
        
        self.action_sequence = self.bfs_to_goal([(self.height - 1, 0)])

        
        if self.action_sequence:
            action = self.action_sequence.pop(0)
            return action

    def make_action(self):
        self.add_safe_cell()

        current_percept = self.get_percept(self.get_position())

        if self.get_health() < 100 and self.get_potion() > 0:
            return "Heal"

        if 'G' in current_percept:
            return "Grab"
        
        if 'H_P' in current_percept:
            return "Grab"

        if 'S' in current_percept:
            direction = self.get_direction()
            i, j = self.get_position()

            index = DIRECTION.index(direction)
            u, v = i + FORWARD[index][0], j + FORWARD[index][1]


            if self.is_valid_move(u, v) and self.is_wumpus[u][v] != False:
                return "Shoot"
            else:
                # check if on the right not safe cell and not shooted
                index = (index + 1) % 4
                u, v = i + FORWARD[index][0], j + FORWARD[index][1]
                if self.is_valid_move(u, v) and self.is_wumpus[u][v] != False:
                    return "Turn Right"
                return "Turn Left"
            
        
        # if there is no None inn safe cell and no unvisited cell --> go back to the start
        if not any(None in row for row in self.safe_cells) and not any(False in row for row in self.visited):
            return self.return_to_start()



        self.action_sequence = self.bfs_to_nearest_safe()

        if self.action_sequence:
            action = self.action_sequence.pop(0)
            return action

        
        
            
            
        # find cell with stench and go there
        print("Health: ", self.get_health())
            
        
        stench_list = []
        for i in range(self.height):
            for j in range(self.width):
                if 'S' in self.grid[i][j]:
                    stench_list.append((i, j))
                    

        if stench_list:
            self.action_sequence = self.bfs_to_goal(stench_list)
            if self.action_sequence:
                action = self.action_sequence.pop(0)
                return action
                    
        
        # go back to start
        return self.return_to_start()
                    
        
            
        
            
        
