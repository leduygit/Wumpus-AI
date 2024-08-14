from logic.map import Map
from logic.Agent.BaseAgent import BaseAgent
from logic.environment import Environment
import logic.CONFIG as CONFIG

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


def simulate():

    for file in CONFIG.FILE_NAME:

        input_file = CONFIG.INPUT_PATH + file + '.txt'
        output_file = CONFIG.OUTPUT_PATH + file + '.json'

        grid = load_map(input_file)
        height = len(grid)
        width = len(grid[0])

        map = Map(grid)
        agent = BaseAgent(width, height)

        env = Environment(map, agent)

        env.simulate()

        env.write_to_file(output_file)

    

