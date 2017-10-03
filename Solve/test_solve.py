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

if __name__ == '__main__':
    main()