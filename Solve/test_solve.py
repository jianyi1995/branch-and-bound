from unittest import TestCase
from unittest import main
from Solve import solve


class TestSolver(TestCase):

    def test_max(self):
        """
        max 3x + 4y
        x + y <= 7
        x - y <= 4
        x >= 0
        y >= 0
        """
        obj = ['max', 3, 4]
        cons = [[1, 1, '<=', 7],
                [1, -1, '<=', 4],
                [1, 0, '>=', 0],
                [0, 1, '>=', 0]]
        s = solve.Solve(2, cons, obj)
        x, opt = s.solve()
        self.assertEqual(x, [0, 7])
        self.assertEqual(opt, 28)

    def test_extreme(self):
        """
        max 3x + 4y
        0 <= 0
        x >= 0
        y >= 0
        """
        obj = ['max', 3, 4]
        cons = [[0, 0, '<=', 0],
                [1, 0, '>=', 0],
                [0, 1, '>=', 0]]
        s = solve.Solve(2, cons, obj)
        x, opt = s.solve()
        self.assertEqual(x, 'infeasible')

    def test_additional_constant(self):
        """
        max 3x + 4y + 7
        x + y <= 7
        x - y <= 4
        x >= 0
        y >= 0
        """
        obj = ['max', 3, 4]
        cons = [[1, 1, '<=', 7],
                [1, -1, '<=', 4],
                [1, 0, '>=', 0],
                [0, 1, '>=', 0]]
        constant = 7
        s = solve.Solve(2, cons, obj, constant)
        x, opt = s.solve()
        self.assertEqual(x, [0, 7])
        self.assertEqual(opt, 35)

    def test_another_max(self):
        """
        max 9x1 + 5x2 + 6x3 + 4x4
        6x1 + 3x2 + 5x3 + 2x4 <= 10
                     x3 + x4 <= 1
        -x1       +  x3      <= 0
            - x2        + x4 <= 0
        0 <= x1, x2, x3, x4 <= 1
        """
        obj = ['max', 9, 5, 6, 4]
        cons = [[6, 3, 5, 2, '<=', 10],
                [0, 0, 1, 1, '<=', 1],
                [-1, 0, 1, 0, '<=', 0],
                [0, -1, 0, 1, '<=', 0],
                [1, 0, 0, 0, '<=', 1],
                [1, 0, 0, 0, '>=', 0],
                [0, 1, 0, 0, '<=', 1],
                [0, 1, 0, 0, '>=', 0],
                [0, 0, 1, 0, '<=', 1],
                [0, 0, 1, 0, '>=', 0],
                [0, 0, 0, 1, '<=', 1],
                [0, 0, 0, 1, '>=', 0]]
        s = solve.Solve(4, cons, obj)
        x, opt = s.solve()
        self.assertEqual(x, [5/6, 1, 0, 1])
        self.assertEqual(opt, 16.5)

    def test_min(self):
        """
        min 3y1 - y2 + 2y3
        2y1 - y2 + y3 >= -1
        y1       + 2y3 >= 2
        -7y1 + 4y2 - 6y3 >= 1
        y1, y2, y3 >= 0
        """
        obj = ['min', 3, -1, 2]
        cons = [[2, -1, 1, '>=', -1],
                [1, 0, 2, '>=', 2],
                [-7, 4, -6, '>=', 1],
                [1, 0, 0, '>=', 0],
                [0, 1, 0, '>=', 0],
                [0, 0, 1, '>=', 0]]
        s = solve.Solve(3, cons, obj)
        x, opt = s.solve()
        self.assertEqual(x, [0, 2, 1])
        self.assertEqual(opt, 0)

    def test_constant(self):
        """
        maximize 14
        0 <= 1 
        """
        obj = ['max', 0]
        cons = [[0, '<=', 1]]
        s = solve.Solve(1, cons, obj, 14)
        x, opt = s.solve()
        self.assertEqual(opt, 14)

    def test_another_constant(self):
        """
        max 20
        2 <= -4
        1 <= 0
        1 <= 1
        """
        obj = ['max', 0]
        cons = [[0, '<=', -6],
                [0, '<=', -1],
                [0, '<=', 0]]
        constant = 20
        s = solve.Solve(1, cons, obj, constant)
        x, opt = s.solve()
        self.assertEqual(x, 'infeasible')

if __name__ == '__main__':
    main()