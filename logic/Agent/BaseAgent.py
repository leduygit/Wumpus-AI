import random

DIRECTION = ['U', 'R', 'D', 'L']

ACTION = ['Foward', 'Turn Left', 'Turn Right', 'Heal']
# F: move forward
# TL: turn left
# TR: turn right
# H: Heal


class BaseAgent:
    def __init__(self, width, height):
        # bottom left corner
        self.position = (height - 1, 0)
        self.direction = 'R'
        self.grid = [[[] for _ in range(width)] for _ in range(height)]
        self.health = 100
        self.score = 0
        self.potion = 0

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
    

    def add_percept(self, position, percept):
        i, j = position
        if (type(percept) == str):
            percept = [percept]

        for p in percept:
            if (p not in self.grid[i][j]):
                self.grid[i][j].append(p)


    def get_position(self):
        return self.position
    
    def get_direction(self):
        return self.direction
    
    def set_position(self, position):
        self.position = position

    def set_direction(self, direction):
        self.direction = direction
    
    def is_valid_move(self, i, j):
        if 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0]):
            return True
        return False
    

    def make_action(self):
        # return random action
        # input the action to the environment

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

