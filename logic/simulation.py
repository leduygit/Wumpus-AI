from map import Map
from Agent.BaseAgent import BaseAgent
from environment import Environment

def main():
    grid = [['', '', '', ''],
            ['', 'W', '', ''],
            ['', 'P', '', ''],
            ['', '', '', '']]
    
    map = Map(grid)
    map.print_map()
    agent = BaseAgent(4, 4)
    env = Environment(map, agent)
    env.simulate()

if __name__ == '__main__':
    main()
