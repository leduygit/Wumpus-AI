# Program class

# wumpus = stench
# pit = breeze
# gold = gold
# P_G = W_H
# H_P = G_L
TYPE = [{'W': 'S'}, {'P': 'B'}, {'P_G': 'W_H'}, {'H_P': 'G_L'}]

class Map:
    def __init__(self, grid):
        self.grid = [[[] for _ in range(len(grid[0]))] for _ in range(len(grid))]
        self.width = len(grid[0])
        self.height = len(grid)

        # update information about stench, breeze, and gold
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j].append(grid[i][j])
                self.update_map_info(i, j)


    def get_grid(self):
        #return a copy of the grid
        return [[self.grid[i][j].copy() for j in range(self.width)] for i in range(self.height)]

    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
    
    def update_map_info(self, i, j):
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for t in TYPE:
            for key, value in t.items():
                if key in self.grid[i][j]:
                    for d in direction:
                        x, y = i + d[0], j + d[1]
                        if 0 <= x < self.height and 0 <= y < self.width:
                            if value not in self.grid[x][y]:
                                self.grid[x][y].append(value)

    def remove_percept(self, cell, percept):
        i, j = cell
        self.grid[i][j].remove(percept)

    def add_percept(self, cell, percept):
        i, j = cell
        self.grid[i][j].append(percept)


    def get_percept(self, cell):
        i, j = cell
        return self.grid[i][j]
    
    def is_valid_move(self, i, j):
        if 0 <= i < self.height and 0 <= j < self.width:
            return True
        return False
    
    def get_neighbors(self, i, j):
        neighbors = []
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in direction:
            x, y = i + d[0], j + d[1]
            if self.is_valid_move(x, y):
                neighbors.append((x, y))
        return neighbors
    
    def print_map(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.grid[i][j], end=' ')
            print()
        print()
    
    