
GAME_OVER = ['W', 'P']

class Environment:
    def __init__(self, map, agent):
        self.map = map
        self.agent = agent

    def is_game_over(self):
        # check if the game is over
        i, j = self.agent.get_position()
        current_cell = self.map.get_percept((i, j))
        for value in current_cell:
            if value in GAME_OVER:
                return True
        return False
    
    
    def simulate(self):
        # simulate the environment
        while True:
            i, j = self.agent.get_position()
            percept = self.map.get_percept((i, j))
            self.agent.add_percept(percept)
            action = self.agent.make_action()
            # print current state of the agent
            print('Agent position:', self.agent.get_position())
            print('Agent direction:', self.agent.get_direction())

            if self.is_game_over():
                break
