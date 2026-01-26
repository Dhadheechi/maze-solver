import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        # print(f"Maze rows: {len(m1._Maze__cells[0])}, Maze columns: {len(m1._Maze__cells)}")
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )
    def test_remove_entry_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._Maze__break_entrance_and_exit()
        # print(f"Maze rows: {len(m1._Maze__cells[0])}, Maze columns: {len(m1._Maze__cells)}")
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._Maze__reset_cells_visited()
        desired = [[False for row in range(num_rows)] for col in range(num_cols)]
        actual = [[cell.visited for cell in col] for col in m1._Maze__cells]
        self.assertEqual(desired, actual)
        
if __name__ == "__main__":
    unittest.main()
