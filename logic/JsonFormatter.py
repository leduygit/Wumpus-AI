import json

class JSonFormatter:
    def __init__(self):
        self.data = {"moves": []}

    def merge_map(self, agent, map):
        # return a new map that merge agent_map and map

        combined_map = map.get_grid()

        
        for i in range(map.get_height()):
            for j in range(map.get_width()):
                # if not visited then add '?' to the cell
                if not agent.get_visited((i, j)):
                    combined_map[i][j].append('?')

        # add agent to the map
        agent_position = agent.get_position()
        combined_map[agent_position[0]][agent_position[1]].append('A')
        return combined_map



    def add_turn(self, map, agent, turn_number, action):
        turn_key = "turn_" + str(turn_number)
        turn_data = {
            turn_key: {
                "map": self.merge_map(agent, map),
                "position": agent.get_position(),
                "action": action,
                "direction": agent.get_direction(),
                "health": agent.get_health(),
                "score": agent.get_score(),
                "potions": agent.get_potion()
            }
        }

        self.data["moves"].append(turn_data)

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)
        