GAME_OVER = ['W', 'P']  # Wumpus and Pit are game-over conditions
DIRECTION = ['U', 'R', 'D', 'L']  # Up, Right, Down, Left

from JsonFormatter import JSonFormatter

class Environment:
    def __init__(self, map, agent):
        self.map = map
        self.agent = agent
        self.game_over = False
        self.formatter = JSonFormatter()

    def is_game_over(self):
        """Check if the game is over based on current cell or agent's health."""
        if self.game_over:
            self.formatter.set_log('Game Over')
            return True

        i, j = self.agent.get_position()
        current_cell = self.map.get_percept((i, j))

        # Check if the agent is in a game-over state
        if any(value in GAME_OVER for value in current_cell):
            # get value in GAME_OVER that is in current_cell

            threat = ''
            for value in GAME_OVER:
                if value in current_cell:
                    threat = value
                    break
            if threat == 'W':
                print('Agent is eaten by Wumpus')
            else:
                print('Agent falls into the pit')
            self.formatter.set_log('Game Over')
            return True

        # Check if the agent's health is depleted
        if self.agent.get_health() <= 0:
            self.formatter.set_log('Game Over')
            return True

        return False

    def remove_percept(self, cell, percept):
        """Remove the specified percept from the given cell."""
        i, j = cell

        # check if there is still no more actuator for the percepts

        PERCEPT_TYPE = {"S": "W", "B": "P", "G_L": "H_P", "P_G": "H_P"}

        if percept in PERCEPT_TYPE:
            actuator = PERCEPT_TYPE[percept]
            # check if there is still no more actuator for the percepts

            for k in range(4):
                di, dj = self.direction_to_delta(DIRECTION[k])
                x, y = i + di, j + dj
                if self.agent.is_valid_move(x, y):
                    if actuator in self.map.get_percept((x, y)):
                        return # do not remove the percept if there is an actuator nearby

        self.map.remove_percept((i, j), percept)
        self.agent.remove_percept((i, j), percept)

    def update_score(self, action):
        """Update the agent's score based on the action taken."""

        # if the agent is killed by the wumpus or falls into the pit -10000
        if self.is_game_over() and not self.game_over:
            self.agent.set_score(self.agent.get_score() - 10000)
            return

        SCORE_MAP = {
            "Forward": -10, "Turn Left": -10, "Turn Right": -10,
            "Heal": -10, "Grab": -10, "Shoot": -100, "Climb": 10
        }

        if action in SCORE_MAP:
            self.agent.set_score(self.agent.get_score() + SCORE_MAP[action])

    def move_agent(self, direction):
        """Move the agent forward in the given direction."""
        i, j = self.agent.get_position()
        di, dj = direction
        new_i, new_j = i + di, j + dj

        if self.agent.is_valid_move(new_i, new_j):
            self.agent.set_position((new_i, new_j))
        else:
            raise ValueError('Invalid move')

    def turn_agent(self, direction_change):
        """Turn the agent left or right."""
        current_direction = DIRECTION.index(self.agent.get_direction())
        new_direction = (current_direction + direction_change) % 4
        self.agent.set_direction(DIRECTION[new_direction])

    def heal_agent(self):
        """Heal the agent if a potion is available."""
        if self.agent.get_potion() > 0:
            self.agent.set_potion(self.agent.get_potion() - 1)
            self.agent.set_health(100)
            print('Health is restored to 100')
        else:
            raise ValueError('No potion to heal')

    def grab_item(self):
        """Grab gold or potion if present in the current cell."""
        i, j = self.agent.get_position()
        current_cell = self.map.get_percept((i, j))

        if 'G' in current_cell:
            self.remove_percept((i, j), 'G')
            self.agent.set_score(self.agent.get_score() + 5000)
            print('Gold is grabbed')
        elif 'H_P' in current_cell:
            self.agent.set_potion(self.agent.get_potion() + 1)
            self.remove_percept((i, j), 'H_P')  # Removing the potion percept
            self.remove_nearby_percept(i, j, 'G_L')  # Removing the glow percept
            print('Potion is grabbed')
        else:
            raise ValueError('No gold or potion to grab')

    def shoot(self):
        """Shoot in the current direction to kill the Wumpus."""
        id = DIRECTION.index(self.agent.get_direction())
        i, j = self.agent.get_position()
        di, dj = self.direction_to_delta(DIRECTION[id])

        if self.agent.is_valid_move(i + di, j + dj):
            if 'W' in self.map.get_percept((i + di, j + dj)):
                self.remove_percept((i + di, j + dj), 'W')
                self.agent.add_percept((i + di, j + dj), 'Sc')
                self.map.set_wumpus_scream(True)
                self.remove_nearby_percept(i + di, j + dj, 'S')  # Removing the stench percept
                print('Wumpus is killed')
            else:
                print('No Wumpus to kill')
        else:
            print('Shoot missed')

    def climb(self):
        """Climb out of the cave if the agent is in the bottom-left corner."""
        if self.agent.get_position() == (self.map.get_height() - 1, 0):
            print('Agent has climbed')
            self.game_over = True
        else:
            raise ValueError('Agent cannot climb')

    def mark_visited(self):
        """Mark the current cell as visited by the agent."""
        i, j = self.agent.get_position()
        self.agent.set_visited((i, j))

    def update_state(self, action):
        """Update the environment state based on the agent's action."""
        if action == "Forward":
            self.move_agent(self.direction_to_delta(self.agent.get_direction()))
        elif action == "Turn Left":
            self.turn_agent(-1)
        elif action == "Turn Right":
            self.turn_agent(1)
        elif action == "Heal":
            self.heal_agent()
        elif action == "Grab":
            self.grab_item()
        elif action == "Shoot":
            self.shoot()
        elif action == "Climb":
            self.climb()

        # only forward action can trigger the poison
        if action == "Forward":
            self.check_for_poison()
        self.update_score(action)
        self.mark_visited()


    def check_for_poison(self):
        """Reduce agent's health if the current cell is poisonous."""
        i, j = self.agent.get_position()
        if "P_G" in self.map.get_percept((i, j)):
            self.agent.set_health(self.agent.get_health() - 25)
            print('Agent is poisoned')

    def remove_nearby_percept(self, i, j, percept):
        """Remove the specified percept from the neighboring cells."""
        for direction in DIRECTION:
            di, dj = self.direction_to_delta(direction)
            x, y = i + di, j + dj
            if self.agent.is_valid_move(x, y):
                if percept in self.map.get_percept((x, y)):
                    self.remove_percept((x, y), percept)

    def direction_to_delta(self, direction):
        """Convert a direction to a movement delta."""
        dir_map = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
        return dir_map[direction]

    def simulate(self):
        """Simulate the environment by continuously updating the agent's state."""
        i, j = self.agent.get_position()
        self.agent.add_percept((i, j), self.map.get_percept((i, j)))
        self.mark_visited()
        self.formatter.add_turn(self.map, self.agent, 0, None)
        turn_number = 1

        while not self.is_game_over():
            action = self.agent.make_action()
            self.update_state(action)
            i, j = self.agent.get_position()
            self.agent.add_percept((i, j), self.map.get_percept((i, j)))
            self.formatter.add_turn(self.map, self.agent, turn_number, action)
            turn_number += 1
            self.map.set_wumpus_scream(False)


    def write_to_file(self, filename):
        """Write the environment state to a JSON file."""
        self.formatter.write_to_file(filename)
