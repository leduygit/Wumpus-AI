
GAME_OVER = ['W', 'P']
DIRECTION = ['U', 'R', 'D', 'L']

class Environment:
    def __init__(self, map, agent):
        self.map = map
        self.agent = agent
        self.game_over = False

    def is_game_over(self):
        # check if the game is over
        if self.game_over:
            return True
        
        i, j = self.agent.get_position()
        current_cell = self.map.get_percept((i, j))
        for value in current_cell:
            if value in GAME_OVER:
                return True
            
        # if health is less than 0
        if self.agent.get_health() <= 0:
            return True
        
        return False
    
    def update_score(self, action):
        SCORE_MAP = {"Forward": -10, "Turn Left": -10, "Turn Right": -10, "Heal": -10, "Grab": -10, "Shoot": -100, "Climb": 10}

        if action in SCORE_MAP:
            self.agent.set_score(self.agent.get_score() + SCORE_MAP[action])

    
    # action = ['Foward', 'Turn Left', 'Turn Right', 'Heal', 'Grab', 'Shoot', 'Climb']
    
    def update_state(self, action):

        i, j = self.agent.get_position()
        dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        if action == "Forward":
            id = DIRECTION.index(self.agent.get_direction())
            if self.agent.is_valid_move(i + dir[id][0], j + dir[id][1]):
                self.agent.set_position((i + dir[id][0], j + dir[id][1]))
            else:
                raise ValueError('Invalid move')
            
        elif action == "Turn Left":
            id = DIRECTION.index(self.agent.get_direction())
            print(id)
            self.agent.set_direction(DIRECTION[(id - 1 + 4) % 4])
            print(self.agent.get_direction())

        elif action == "Turn Right":
            id = DIRECTION.index(self.agent.get_direction())
            print(id)
            self.agent.set_direction(DIRECTION[(id + 1) % 4])
            print(self.agent.get_direction())

        elif action == "Heal":
            if self.agent.get_potion() > 0:
                self.agent.set_potion(self.agent.get_potion() - 1)
                self.agent.set_health(100)
                print('Health is restored to 100')
            else:
                raise ValueError('No potion to heal')

        elif action == "Grab":
            if 'G' in self.map.get_percept((i, j)):
                self.map.remove_percept((i, j), 'G')
                self.agent.remove_percept((i, j), 'G')
                self.agent.set_score(self.agent.get_score() + 5000)
                print('Gold is grabbed')
            elif  'H_P' in self.map.get_percept((i, j)):
                self.agent.set_potion(self.agent.get_potion() + 1)
                self.agent.remove_percept((i, j), 'H_P')
                self.map.remove_percept((i, j), 'H_P')
                # remove G_L percept

                for k in range(len(dir)):
                    x, y = i + dir[k][0], j + dir[k][1]
                    if self.agent.is_valid_move(x, y):
                        if 'G_L' in self.map.get_percept((x, y)):
                            self.map.remove_percept((x, y), 'G_L')
                            self.agent.remove_percept((x, y), 'G_L')

                print('Potion is grabbed')
            else:
                raise ValueError('No gold or potion to grab')

        elif action == "Shoot":
            # add scream percept and remove wumpus if wumpus is killed, remove stench percept
            id = DIRECTION.index(self.agent.get_direction())
            i, j = self.agent.get_position()

            
            # remove wumpus in that cell and add scream percept if wumpus is killed to that cell
            if self.agent.is_valid_move(i + dir[id][0], j + dir[id][1]):
                if 'W' in self.map.get_percept((i + dir[id][0], j + dir[id][1])):
                    self.map.remove_percept((i + dir[id][0], j + dir[id][1]), 'W')
                    self.agent.remove_percept((i + dir[id][0], j + dir[id][1]), 'W')

                    u, v = i + dir[id][0], j + dir[id][1]
                    self.agent.add_percept((u, v), 'Sc')

                    # remove stench percept from neightbor of (u, v)

                    for k in range(len(dir)):
                        x, y = u + dir[k][0], v + dir[k][1]
                        if self.agent.is_valid_move(x, y):
                            if 'S' in self.map.get_percept((x, y)):
                                self.map.remove_percept((x, y), 'S')
                                self.agent.remove_percept((x, y), 'S')

                    print('Wumpus is killed')
                else:
                    print('No wumpus to kill')


        elif action == "Climb":
            # if the agent is at the bottom left corner, then the agent can climb
            if self.agent.get_position() == (self.map.get_height() - 1, 0):
                print('Agent has climbed')
                self.game_over = True
            else:
                raise ValueError('Agent cannot climb')
        
        # if current cell is poisonous, then agent health is reduced by 25
        
        i, j = self.agent.get_position()
        if ("P_G" in self.map.get_percept((i, j))):
            self.agent.set_health(self.agent.get_health() - 25)
            print('Agent is poisoned')
            

        self.update_score(action)

        print('Agent information:')
        self.agent.print_agent_info()


    
    
    def simulate(self):
        # simulate the environment
        i, j = self.agent.get_position()    
        self.agent.add_percept((i, j), self.map.get_percept((i, j)))

        print('Agent information:')
        self.agent.print_agent_info()

        
        while True:
            action = self.agent.make_action()
            self.update_state(action)
            
            i, j = self.agent.get_position()

            percept = self.map.get_percept((i, j))

            self.agent.add_percept((i, j), percept)

            if self.is_game_over():
                break
