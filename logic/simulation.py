from map import Map
from Agent.BaseAgent import BaseAgent
from environment import Environment

# the map is represented as a grid
# each cell is seperated by a dot
# empty cell is '-'
# example:
# -.-.-.-
# -.W.-.-
# -.P.-.-
# -.-.-.-

def load_map(file):
    grid = []
    with open(file, 'r') as f:
        for line in f:
            grid.append(line.strip().split('.'))
    return grid

def main():
    grid = load_map('map.txt')
    
    map = Map(grid)
    map.print_map()
    agent = BaseAgent(4, 4)
    env = Environment(map, agent)
    env.simulate()
    env.write_to_file('output.json')

if __name__ == '__main__':
    main()
