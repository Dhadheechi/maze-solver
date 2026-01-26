from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        # self.__root.configure(bg="white")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack(fill=BOTH, expand=True)
        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def draw(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def get_bg_color(self):
        return self.__canvas["bg"]


    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2,):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="white"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, window=None):
        self.window = window
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_left_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1 # these values define the boundaries of the cell
        self.visited = False

    def draw(self, x1, y1, x2, y2, fill_color="black"):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.window:
            bg = self.window.get_bg_color()
            if self.has_left_wall:
                self.window.draw(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), fill_color)
            else:
                self.window.draw(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), bg)
            if self.has_right_wall:
                self.window.draw(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), fill_color)
            else:
                self.window.draw(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), bg)
            if self.has_top_wall:
                self.window.draw(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), fill_color)
            else:
                self.window.draw(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), bg)

            if self.has_bottom_wall:
                self.window.draw(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), fill_color)
            else:
                self.window.draw(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), bg)


    def draw_move(self, to_cell, undo=False):
        x1 = (self.__x1 + self.__x2) / 2
        y1 = (self.__y1 + self.__y2) / 2
        x2 = (to_cell.__x1 + to_cell.__x2) / 2
        y2 = (to_cell.__y1 + to_cell.__y2) / 2

        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
       
        fill_color = "red"
        if undo:
            fill_color = "gray"
        if self.window:
            self.window.draw(Line(p1, p2), fill_color)            




class Maze: # holds all the cells in a list of lists
    def __init__(self, x1, y1, rows, cols, cell_size_x, cell_size_y, win=None, seed=None):
        if seed:
            random.seed(seed)
        self.x1 = x1
        self.y1 = y1
        self.rows = rows
        self.cols = cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.__cells = []
        self.__create_cells()

        if seed:
            random.seed(seed)

    def __create_cells(self):
        self.__cells = [[Cell(self.win) for _ in range(self.rows)] for _ in range(self.cols)] # [i][j] refers to the ith column and the jth row instead of the other way round
        for col_index, col in enumerate(self.__cells):
            for row_index, row in enumerate(col):
                self.__draw_cell(col_index, row_index)

    def __draw_cell(self, i, j):
        x1 = self.x1 + i * self.cell_size_x
        x2 = self.x1 + (i + 1) * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        y2 = self.y1 + (j + 1) * self.cell_size_y

        if self.win:
            self.__cells[i][j].draw(x1, y1, x2, y2)
            self.__animate()

    def __animate(self):
        self.win.redraw()
        time.sleep(0.005)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0) # udpating the removal
        self.__cells[self.cols - 1][self.rows - 1].has_bottom_wall = False
        self.__draw_cell(self.cols - 1, self.rows - 1) 


    def __break_walls_r(self, i, j):
        current_cell = self.__cells[i][j]
        current_cell.visited = True
        while True:
            neighbours = []
            if current_cell.has_left_wall and i != 0:
                neighbour = self.__cells[i-1][j]
                if not neighbour.visited:
                    neighbours.append((i-1, j))
            if current_cell.has_right_wall and i != self.cols - 1:
                neighbour = self.__cells[i+1][j]
                if not neighbour.visited:
                    neighbours.append((i+1, j))
            if current_cell.has_top_wall and j != 0:
                neighbour = self.__cells[i][j-1]
                if not neighbour.visited:
                    neighbours.append((i, j-1))
            if current_cell.has_bottom_wall and j != self.rows - 1:
                neighbour = self.__cells[i][j+1]
                if not neighbour.visited:
                    neighbours.append((i, j + 1))
            
            if len(neighbours) == 0: # no directions available
                self.__draw_cell(i, j)
                return 

            direction = random.choice(neighbours)
            x, y = direction[0], direction[1]
            neighbour = self.__cells[x][y]
            if i - x == 1 and j - y == 0:
                self.__cells[i][j].has_left_wall = False
                self.__cells[x][y].has_right_wall = False
                self.__draw_cell(i, j)
                # self.__draw_cell(x,y)
                self.__break_walls_r(x, y)
            elif x - i == 1 and j - y == 0:
                self.__cells[i][j].has_right_wall = False
                self.__cells[x][y].has_left_wall = False
                self.__draw_cell(i, j)
                # self.__draw_cell(x,y)
                self.__break_walls_r(x, y)
            elif i - x == 0 and j - y == -1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[x][y].has_top_wall = False
                self.__draw_cell(i, j)
                # self.__draw_cell(x,y)
                self.__break_walls_r(x, y)
            elif i - x == 0 and j - y == 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[x][y].has_bottom_wall = False
                self.__draw_cell(i, j)
                # self.__draw_cell(x,y)
                self.__break_walls_r(x, y)

    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self.__animate()
        current_cell = self.__cells[i][j]
        current_cell.visited = True
        if i == self.cols - 1 and j == self.rows - 1:
            return True
        directions = ["left", "right", "up", "down"]
        for direction in directions:
            if direction == "left":
                if not current_cell.has_left_wall and i != 0:
                    left_cell = self.__cells[i-1][j]
                    if not left_cell.visited: 
                        current_cell.draw_move(left_cell)
                        if self._solve_r(i-1, j):
                            return True
                        current_cell.draw_move(left_cell, undo=True)
            if direction == "right":
                if not current_cell.has_right_wall and i != self.cols - 1:
                    right_cell = self.__cells[i+1][j]
                    if not right_cell.visited:
                        current_cell.draw_move(right_cell)
                        if self._solve_r(i+1, j):
                            return True
                        current_cell.draw_move(right_cell, undo=True)
            if direction == "up" and j != 0:
                if not current_cell.has_top_wall:
                    top_cell = self.__cells[i][j-1]
                    if not top_cell.visited: 
                        current_cell.draw_move(top_cell)
                        if self._solve_r(i, j-1):
                            return True
                        current_cell.draw_move(top_cell, undo=True)
            if direction == "down" and j != self.rows - 1:
                if not current_cell.has_bottom_wall:
                    down_cell = self.__cells[i][j+1]
                    if not down_cell.visited:
                        current_cell.draw_move(down_cell)
                        if self._solve_r(i, j+1):
                            return True
                        current_cell.draw_move(down_cell, undo=True)
            
        return False




def main():
    win = Window(800, 600)
    m = Maze(100, 100, 20, 20, 20, 20, win)
    m._Maze__break_entrance_and_exit()
    m._Maze__break_walls_r(10, 10)
    m._Maze__reset_cells_visited()
    m.solve()
    # m = Maze(100, 100, 3, 3, 20, 20, win)
    # m._Maze__break_entrance_and_exit()
    # m._Maze__break_walls_r(1, 1)
    # m._Maze__reset_cells_visited()
    win.wait_for_close()


if __name__ == "__main__":
    main()
