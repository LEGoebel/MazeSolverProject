import unittest
from classes import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_large(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_entry_top_wall_false(self):
        num_cols = 35
        num_rows = 25
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertTrue(
            m1._cells[0][0].has_top_wall == False
        )

    def test_maze_exit_bottom_wall_false(self):
        num_cols = 35
        num_rows = 25
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertTrue(
            m1._cells[-1][-1].has_bottom_wall == False
        )

    def test_maze_exit_bottom_wall_false(self):
        num_cols = 35
        num_rows = 25
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        for col in m1._cells:
            for cell in col:
                self.assertEqual(
                    cell._visited,
                    False

        )
        


if __name__ == "__main__":
    unittest.main()