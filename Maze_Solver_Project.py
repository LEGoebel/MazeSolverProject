from classes import *
import sys



def main():
    num_rows = 25
    num_cols = 30
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    sys.setrecursionlimit(10000)

    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    is_solvable = maze.solve()
    if not is_solvable:
        print("Labyrinth kann nicht gelöst werden! Dieser Fall sollte eigentlich nicht eintreffen >.<")
    else:
        print("Labyrinth gelöst!")

    win.wait_for_close()


main()

