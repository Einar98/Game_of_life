import pygame 
import random
"Conways game of life simulation" 
"Rules: "
"1. Any live cell with fewer than two live neighbours dies, as if by underpopulation. "
"2. Any live cell with two or three live neighbours lives on to the next generation. "
"3. Any live cell with more than three live neighbours dies, as if by overpopulation. "
"4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction."

class Cell:
    def __init__(self, coords:tuple, dim_length:int, max_x:int, max_y:int) -> None:
        self.is_alive = False 
        self.coords = coords 
        self.dim_length = dim_length
        self.max_x = max_x 
        self.max_y = max_y
        self.neighbour_coords = self.get_coords_of_neighbours() 
        self.alive_color = (255, 255, 255) 
        self.dead_color = (0, 0, 0)
    
    def draw(self, window) -> None:
        if self.is_cell_alive():
            self.draw_alive(window) 
        else:
            self.draw_dead(window)

    # Draws a white square onto the window. 
    def draw_alive(self, window) -> None:
        x, y = self.coords 
        x_coord = x * self.dim_length 
        y_coord = y * self.dim_length 
        pygame.draw.rect(window, self.alive_color, [x_coord, y_coord, self.dim_length, self.dim_length])  

    # Draws a black square onto the window. 
    def draw_dead(self, window) -> None:
        x, y = self.coords 
        x_coord = x * self.dim_length 
        y_coord = y * self.dim_length 
        pygame.draw.rect(window, self.dead_color, [x_coord, y_coord, self.dim_length, self.dim_length])  
    
    # Checks if a cell is alive or dead. 
    def is_cell_alive(self) -> bool:
        return self.is_alive
    
    def change_to_alive(self) -> None:
        self.is_alive = True 

    def change_to_dead(self) -> None:
        self.is_alive = False 
    
    # Returns the coords of the cell.
    def get_coords(self) -> tuple:
        return self.coords
    
    def has_left_neighbour(self) -> bool:
        x, y = self.get_coords() 
        if x-1 >= 0:
            return True 
        return False 
    
    def has_right_neighbour(self) -> bool:
        x, y = self.get_coords() 
        if x + 1 < self.max_x:
            return True 
        return False 
    
    def has_upper_neighbour(self) -> bool:
        x, y = self.get_coords() 
        if y-1 >= 0:
            return True 
        return False 
    
    def has_lower_neighbour(self) -> bool:
        x, y = self.get_coords() 
        if y + 1 < self.max_y:
            return True 
        return False 
    
    def has_upper_left_neighbour(self) -> bool:
        x, y = self.get_coords() 
        if x-1 >= 0 and y-1 >= 0:
            return True 
        return False 

    def has_upper_right_neighbour(self) -> bool:
        x, y = self.get_coords() 
        if y-1 >= 0 and x + 1 < self.max_x:
            return True 
        return False 

    def has_lower_left_neighbour(self) -> bool:
        x, y = self.get_coords()
        if x-1 >= 0 and y+1 < self.max_y:
            return True 
        return False  
    
    def has_lower_right_neighbour(self) -> bool:
        x, y = self.get_coords() 
        if x + 1 < self.max_x and y + 1 < self.max_y:
            return True 
        return False
    
    def get_coords_of_neighbours(self) -> list:
        neighbour_coords = [] 
        x, y = self.get_coords()
        if self.has_right_neighbour():
            neighbour_coords.append((x + 1, y))
        if self.has_left_neighbour():
            neighbour_coords.append((x-1, y)) 
        if self.has_lower_left_neighbour():
            neighbour_coords.append((x-1, y+1))
        if self.has_lower_right_neighbour():
            neighbour_coords.append((x+1, y+1))
        if self.has_upper_neighbour():
            neighbour_coords.append((x, y-1))
        if self.has_lower_neighbour():
            neighbour_coords.append((x, y+1)) 
        if self.has_upper_left_neighbour():
            neighbour_coords.append((x-1, y-1))
        if self.has_upper_right_neighbour():
            neighbour_coords.append((x+1, y-1)) 
        return neighbour_coords
    
    def count_alive_neighbours(self, grid) -> int:
        alive_cells = 0 
        for cell in grid:
            # Check if its a neighbour. 
            if cell.get_coords() in self.neighbour_coords and cell.is_cell_alive():
                alive_cells += 1 
        return alive_cells

class Grid:
    def __init__(self, x_cells:int, y_cells:int, dim_length:int) -> None:
        self.x_cells = x_cells 
        self.y_cells = y_cells 
        self.dim_length = dim_length 
        self.cells = self.create_list_of_cells()
        self.randomize_dead_and_alive()
        self.window_height = y_cells * dim_length 
        self.window_width = x_cells * dim_length 
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.background_color = (255, 255, 255)
        self.grid_lines_color = (100, 100, 100)
        self.FPS = 5 
        self.clock = pygame.time.Clock()

    # Creates a list of cells. 
    def create_list_of_cells(self) -> tuple:
        cells = [] 
        for y in range(self.y_cells):
            for x in range(self.x_cells):
                 cells.append(Cell((x, y), self.dim_length, self.x_cells, self.y_cells))
        return cells

    # Randomly sets the cells to either dead or alive. 
    def randomize_dead_and_alive(self) -> None:
        for cell in self.cells:
            if random.randint(0, 1) == 0:
                cell.change_to_alive()
            else:
                cell.change_to_dead() 

    # Gets the cell count of the grid. 
    def get_cell_count(self) -> int:
        return len(self.cells)

    # Updates the grid based on the rules. 
    def update_grid(self) -> list:
        new_grid = [] 
        for cell in self.cells:
            # Count the number of alive neighbours next to this cell. 
            alive_neighbour_cells = cell.count_alive_neighbours(self.cells) 
            cell_coords = cell.get_coords()
            # New cell is dead. 
            if cell.is_cell_alive() and alive_neighbour_cells < 2:
                new_grid.append(Cell(cell_coords, self.dim_length, self.x_cells, self.y_cells))
            # New cell is alive. 
            elif cell.is_cell_alive() and 2 <= alive_neighbour_cells <= 3:
                new_cell = Cell(cell_coords, self.dim_length, self.x_cells, self.y_cells) 
                new_cell.change_to_alive() 
                new_grid.append(new_cell)  
            # New cell is dead. 
            elif cell.is_cell_alive() and alive_neighbour_cells > 3:
                new_grid.append(Cell(cell_coords, self.dim_length, self.x_cells, self.y_cells)) 
            # New cell is alive. 
            elif not cell.is_cell_alive() and alive_neighbour_cells == 3:
                new_cell = Cell(cell_coords, self.dim_length, self.x_cells, self.y_cells) 
                new_cell.change_to_alive() 
                new_grid.append(new_cell)
            # If doesnt meet any of these conditions, do nothing. 
            else:
                new_grid.append(cell)
        return new_grid
    
    def draw_grid_lines(self) -> None:
        # Draws the vertical lines. 
        for i in range(self.x_cells):
            p1 = (i * self.dim_length, 0) 
            p2 = (i * self.dim_length, self.window_height) 
            width = 2 
            pygame.draw.line(self.window, self.grid_lines_color, p1, p2, width) 
        # Draws the horizontal lines. 
        for j in range(self.y_cells):
            p3 = (0, j * self.dim_length) 
            p4 = (self.window_width, j * self.dim_length) 
            width = 2 
            pygame.draw.line(self.window, self.grid_lines_color, p3, p4, width)
    
    # Draws all the cells onto the window. 
    def draw_cells(self) -> None:
        for cell in self.cells:
            cell.draw(self.window)

    # Prints the different cells, if they're alive or not. 
    def print_alive_and_dead_cells(self) -> None:
        for cell in self.cells:
            if cell.is_cell_alive():
                print("Alive") 
            else:
                print("Dead")

    def simulate(self) -> None:
        running = True 
        while running:
            self.window.fill(self.background_color) 
            self.draw_grid_lines()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
            # Run simulation here. 
            # Draw the cells. 
            self.draw_cells() 
            # Update the new cells 
            self.cells = self.update_grid() 
            pygame.display.update()
            self.clock.tick(self.FPS)

# Constants 
X_CELLS = 25 
Y_CELLS = 25 
DIM_LENGTH = 20 

my_grid = Grid(X_CELLS, Y_CELLS, DIM_LENGTH) 
my_grid.simulate()

