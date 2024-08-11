import json

SENSE = {"S": "Stench", "B": "Breeze", "G_L": "Glow", "W_H": "Whiff"}

class JSonFormatter:
    def __init__(self):
        self.data = []
        self.log = ''

    def set_log(self, log):
        self.log = log

    def get_log(self, agent, map):
        # return the log of the agent
        if self.log != '':
            return self.log

        # if game is over then return the game over message

        log = []
        i, j = agent.get_position()

        # check if wumpus is screaming
        if (map.get_wumpus_scream()):
            log.append("Scream")
        

        # get the percept of the agent of current cell
        percept = map.get_percept((i, j))
        for p in percept:
            if p in SENSE:
                log.append(SENSE[p])
        
        # connect the sense by ','
        message = "Sense " + ', '.join(log)
        if len(log) == 0:
            message = "Sense None"
        return message


    def merge_map(self, agent, map):
        # return a new map that merge agent_map and map

        combined_map = map.get_grid()

        
        for i in range(map.get_height()):
            for j in range(map.get_width()):
                # if not visited then add '?' to the cell
                if not agent.get_visited((i, j)):
                    combined_map[i][j].append('?')

        # add door to the map at beginning position
        i, j = map.get_height() - 1, 0
        combined_map[i][j].append('D')

        return combined_map




    def add_turn(self, map, agent, turn_number, action):
        current_position = agent.get_position()

        if action == None:
            action = "None"

        turn_data = {
            "turn": str(turn_number),
            "map": self.merge_map(agent, map),
            "position": [str(current_position[0]), str(current_position[1])],
            "action": action,
            "direction": agent.get_direction(),
            "health": str(agent.get_health()),
            "score": str(agent.get_score()),
            "potion": str(agent.get_potion()),
            "log": self.get_log(agent, map)
        }

        self.data.append(turn_data)

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)
        