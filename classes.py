from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title('Maze Solver Project')
        self.canvas = Canvas(self.__root, bg="white", height=self.height, width=self.width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()
        print("window closed...")

    def close(self):
        self.running = False


class Point:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

class Line:
    def __init__(self, startpoint, endpoint):
        self.startpoint = startpoint
        self.endpoint = endpoint

    def draw(self, canvas, fill_color):
        canvas.create_line(self.startpoint.x_coord, self.startpoint.y_coord, self.endpoint.x_coord, self.endpoint.y_coord, fill = fill_color, width = 2)

class Cell():
    def __init__(self, win = None):
            self.has_left_wall = True
            self.has_right_wall = True
            self.has_top_wall = True
            self.has_bottom_wall = True
            self._x1 = None
            self._x2 = None
            self._y1 = None
            self._y2 = None
            self._win = win
            self._visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        if not self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, fill_color = "white")
        if not self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, fill_color = "white")
        if not self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, fill_color = "white")
        if not self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, fill_color = "white")

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo == True: color = "grey"
        x_self_center = (self._x2 + self._x1)/2
        y_self_center = (self._y2 + self._y1)/2
        x_target_center = (to_cell._x2 + to_cell._x1)/2
        y_target_center = (to_cell._y2 + to_cell._y1)/2
        Line(Point(x_self_center, y_self_center),Point(x_target_center, y_target_center)).draw(self._win.canvas, color)

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = None
        if seed != None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls(0,0)
        self._reset_cells_visited()


    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            tmp = []
            for j in range(self.num_rows):
                tmp_cell = Cell(self.win)
                tmp.append(tmp_cell)
            self._cells.append(tmp)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i,j)

    def _draw_cell(self, i, j):
        if None == self.win: return
        top_left_corner_cell_x = self.x1 + i * self.cell_size_x
        top_left_corner_cell_y = self.y1 + j * self.cell_size_y
        bottom_right_corner_cell_x = top_left_corner_cell_x + self.cell_size_x
        bottom_right_corner_cell_y = top_left_corner_cell_y + self.cell_size_y

        self._cells[i][j].draw(top_left_corner_cell_x,top_left_corner_cell_y, bottom_right_corner_cell_x, bottom_right_corner_cell_y)
        self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self.num_cols -1, self.num_rows -1)

    def _break_walls(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            cells_to_visit = []
            #Grenzen des Labyrinths bewahren und prüfen, welche adjazenten Zellen noch nicht besucht waren.
            if i > 0 and not self._cells[i - 1][j]._visited:
                cells_to_visit.append((i-1, j))
            if i < self.num_cols - 1 and not self._cells[i+1][j]._visited:
                cells_to_visit.append((i+1, j))
            if j > 0 and not self._cells[i][j-1]._visited:
                cells_to_visit.append((i, j-1))
            if j < self.num_rows - 1 and not self._cells[i][j+1]._visited:
                cells_to_visit.append((i,j+1))


            #Breakout, wenn keine Zellen mehr zu besuchen sind
            if len(cells_to_visit) == 0:
                self._draw_cell(i, j)
                return

            #Zufällige Richtung wählen
            direction_to_go = random.randrange(len(cells_to_visit))
            next_index = cells_to_visit[direction_to_go]

            #Wände löschen
            # rechts
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # links
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # unten
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # oben
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            #Rekursion zum weitergehen
            self._break_walls(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j]._visited = False

    def _solve_r(self, i, j):
        self._animate()

        self._cells[i][j]._visited = True
        
        if self.num_cols -1 == i and self.num_rows - 1 == j:
            print("Ende des Labyrinths erreicht!")
            return True

        #prüfen, ob nach links korrekter Weg weitergeht
        if (i > 0 
            and not self._cells[i][j].has_left_wall 
            and not self._cells[i - 1][j]._visited):
            #print(f"Attempting move left from ({i}, {j}) to ({i - 1}, {j})")
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                #print(f"Backtracking from ({i - 1}, {j}) to ({i}, {j})")
                self._cells[i][j].draw_move(self._cells[i-1][j], undo = True)

        #prüfen, ob nach rechts korrekter Weg weitergeht
        if (i < self.num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j]._visited):
            #print(f"Attempting move right from ({i}, {j}) to ({i + 1}, {j})")
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                #print(f"Backtracking from ({i + 1}, {j}) to ({i}, {j})")
                self._cells[i][j].draw_move(self._cells[i+1][j], undo = True)

        #prüfen, ob nach oben korrekter Weg weitergeht
        if (j > 0 
            and not self._cells[i][j].has_top_wall 
            and not self._cells[i][j - 1]._visited):
            #print(f"Attempting move up from ({i}, {j}) to ({i}, {j-1})")
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                #print(f"Backtracking from ({i}, {j-1}) to ({i}, {j})")
                self._cells[i][j].draw_move(self._cells[i][j-1], undo = True)

        #prüfen, ob nach unten korrekter Weg weitergeht
        if (j < self.num_rows - 1 
            and not self._cells[i][j].has_bottom_wall 
            and not self._cells[i][j + 1]._visited):
            #print(f"Attempting move up from ({i}, {j}) to ({i}, {j+1})")
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                #print(f"Backtracking from ({i}, {j+1}) to ({i}, {j})")
                self._cells[i][j].draw_move(self._cells[i][j+1], undo = True)
        
        return False
    
    def solve(self):
        return self._solve_r(0, 0)
                
                
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.005)
