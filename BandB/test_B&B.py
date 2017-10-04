from unittest import TestCase
from unittest import main
from BandB import bandb


class TestSolver(TestCase):

    def test_is_int_none(self):
        s = bandb.BandB(0, 0, 0, 0)
        solution = [1.00000, 2, 3, 4.0, -2.0]
        self.assertEqual(s.is_int(solution), None)

    def test_is_int(self):
        s = bandb.BandB(0, 0, 0, 0)
        solution = [1.0000000000000, 2, 3, 4.5]
        self.assertEqual(s.is_int(solution), 3)

    def test_get_current_lp_with_1(self):
        """
        max 3x1 + 4x2 + 6x3
        x1 + x2 + x3<= 5
        x1 >= 0
        x2 >= 0
        x3 >= 0
        x3 = 1
        """
        origin_number = 3
        origin_cons = [[1, 1, 1, '<=', 5],
                [1, 0, 0, '>=', 0],
                [0, 1, 0, '>=', 0],
                [0, 0, 1, '>=', 0]]
        origin_obj = ['max', 3, 4, 6]
        fixed = [-1, -1, 1]
        s = bandb.BandB(origin_number, origin_cons, origin_obj)
        number, cons, obj, constant = s.get_current_lp(fixed)
        self.assertEqual(number, 2)
        self.assertEqual(cons, [[1, 1, '<=', 4],
                                [1, 0, '>=', 0],
                                [0, 1, '>=', 0],
                                [0, 0, '>=', -1]])
        self.assertEqual(obj, ['max', 3, 4])
        self.assertEqual(constant, 6)

    def test_get_current_lp_with_0(self):
        """
        max 3x1 + 4x2 + 6x3
        x1 + x2 + x3<= 5
        x1 >= 0
        x2 >= 0
        x3 >= 0
        x3 = 0
        """
        origin_number = 3
        origin_cons = [[1, 1, 1, '<=', 5],
                       [1, 0, 0, '>=', 0],
                       [0, 1, 0, '>=', 0],
                       [0, 0, 1, '>=', 0]]
        origin_obj = ['max', 3, 4, 6]
        fixed = [-1, -1, 0]
        s = bandb.BandB(origin_number, origin_cons, origin_obj)
        number, cons, obj, constant = s.get_current_lp(fixed)
        self.assertEqual(number, 2)
        self.assertEqual(cons, [[1, 1, '<=', 5],
                                [1, 0, '>=', 0],
                                [0, 1, '>=', 0],
                                [0, 0, '>=', 0]])
        self.assertEqual(obj, ['max', 3, 4])
        self.assertEqual(constant, 0)

    def test_get_current_lp_with_0_and_1(self):
        """
        max 3x1 + 4x2 + 6x3
        x1 + x2 + x3<= 5
        x1 >= 0
        x2 >= 0
        x3 >= 0
        x2 = 0
        x3 = 1
        """
        origin_number = 3
        origin_cons = [[1, 1, 1, '<=', 5],
                       [1, 0, 0, '>=', 0],
                       [0, 1, 0, '>=', 0],
                       [0, 0, 1, '>=', 0]]
        origin_obj = ['max', 3, 4, 6]
        fixed = [-1, 0, 1]
        s = bandb.BandB(origin_number, origin_cons, origin_obj)
        number, cons, obj, constant = s.get_current_lp(fixed)
        self.assertEqual(number, 1)
        self.assertEqual(cons, [[1, '<=', 4],
                                [1, '>=', 0],
                                [0, '>=', 0],
                                [0, '>=', -1]])
        self.assertEqual(obj, ['max', 3])
        self.assertEqual(constant, 6)

if __name__ == '__main__':
    main()
