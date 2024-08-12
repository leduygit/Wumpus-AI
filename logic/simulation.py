from map import Map
from Agent.BaseAgent import BaseAgent
from environment import Environment

# the map is represented as a grid
# each cell is seperated by a dot
# empty cell is '-'
# example:

# 4
# -.-.-.-
# -.W, G.-.-
# -.P.-.-
# -.-.-.-

def load_map(file):
    with open(file, 'r') as f:
        lines = f.readlines()

        # The first line contains the size of the grid, so we ignore it

        grid = []
        for line in lines[1:]:  # Start from the second line
            row = []
            elements = line.strip().split('.')
            for element in elements:
                if ',' in element:
                    row.append(element.split(','))
                else:
                    row.append(element)
            grid.append(row)
    return grid


def main():
    grid = load_map('map.txt')
    
    map = Map(grid)
    map.print_map()

    size = len(grid)
    agent = BaseAgent(size, size)
    env = Environment(map, agent)
    env.simulate()
    env.write_to_file('output.json')

if __name__ == '__main__':
    main()
