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

    def test_add_active_with_empty_queue(self):
        """
        assume:
        self.queue = {}
        fixed = [-1, -1, -1] solution = [1, 0, 0.5] opt = 16 the element that needs to be branched is the third, 
        so index is 2, and queue should be 16: [[-1, -1, 0], [-1, -1, 1]]
        """
        s = bandb.BandB(0, 0, 0)
        fixed = [-1, -1, -1]
        opt = 16
        index = 2
        s.add_active(fixed, index, opt)
        self.assertEqual(s.queue, {16: [[-1, -1, 0], [-1, -1, 1]]})

    def test_add_active_with_non_empty_queue(self):
        """
        assume:
        self.queue = {16:[[-1, 0, 1]]}
        fixed = [-1, -1, -1] solution = [1, 0, 0.5] opt = 16 the element that needs to be branched is the third, 
        so index is 2, and queue should be 16: [[-1, 0, 1], [-1, -1, 0], [-1, -1, 1]]
        """
        s = bandb.BandB(0, 0, 0)
        fixed = [-1, -1, -1]
        opt = 16
        index = 2
        s.queue = {16: [[-1, 0, 1]]}
        s.add_active(fixed, index, opt)
        self.assertEqual(s.queue, {16: [[-1, 0, 1], [-1, -1, 0], [-1, -1, 1]]})

    def test_get_active(self):
        """
        assume:
        self.queue = {16:[[-1, 0, 1], [1, 0, 1]], 14: [[-1, 0, 1]]}
        no add operation,
        after first get, it should return [-1, 0, 1], the queue becomes {16: [[1, 0, 1]], 14: [[-1, 0, 1]]}
        the second get, it should return [1, 0, 1], the queue becomes {14: [[-1, 0, 1]]}
        the third one, it should return [-1, 0, 1], the queue becomes empty
        """
        s = bandb.BandB(0, 0, 0)
        s.queue = {16: [[-1, 0, 1], [1, 0, 1]], 14: [[-1, 0, 1]]}
        fixed = s.get_active()
        self.assertEqual(fixed, [-1, 0, 1])
        self.assertEqual(s.queue, {16: [[1, 0, 1]], 14: [[-1, 0, 1]]})
        fixed = s.get_active()
        self.assertEqual(fixed, [1, 0, 1])
        self.assertEqual(s.queue, {14: [[-1, 0, 1]]})
        fixed = s.get_active()
        self.assertEqual(fixed, [-1, 0, 1])
        self.assertEqual(s.queue, {})

    def test_add_and_get_active(self):
        """
        assume:
        self.queue = {16: [[1, 0, 1]]}
        after one get ,one add and then two get operations
        """
        s = bandb.BandB(0, 0, 0)
        s.queue = {16: [[1, 0, 1]]}
        fixed = s.get_active()
        self.assertEqual(fixed, [1, 0, 1])
        self.assertEqual(s.queue, {})
        s.add_active([-1, 0, -1], 1, 16)
        self.assertEqual(s.queue, {16: [[-1, 0, 0], [-1, 0, 1]]})
        fixed = s.get_active()
        self.assertEqual(fixed, [-1, 0, 0])
        self.assertEqual(s.queue, {16: [[-1, 0, 1]]})
        fixed = s.get_active()
        self.assertEqual(fixed, [-1, 0, 1])
        self.assertEqual(s.queue, {})

    def test_init(self):
        """
        max 9x1 + 5x2 + 6x3 + 4x4
        6x1 + 3x2 + 5x3 + 2x4 <= 10
                     x3 +  x4 <= 1
        -x1       +  x3       <= 0
              -x2       +  x4 <= 0
        0 <= x1, x2, x3, x4 <= 1
        after the first computing, the solution, opt are (5/6, 1, 0, 1) and 16.5
        so the queue will become {16.5: [[0, -1, -1, -1], [1, -1, -1, -1]]}
        """
        number = 4
        cons = [[6, 3, 5, 2, '<=', 10],
                [0, 0, 1, 1, '<=', 1],
                [-1, 0, 1, 0, '<=', 0],
                [0, -1, 0, 1, '<=', 0],
                [1, 0, 0, 0, '>=', 0],
                [1, 0, 0, 0, '<=', 1],
                [0, 1, 0, 0, '>=', 0],
                [0, 1, 0, 0, '<=', 1],
                [0, 0, 1, 0, '>=', 0],
                [0, 0, 1, 0, '<=', 1],
                [0, 0, 0, 1, '>=', 0],
                [0, 0, 0, 1, '<=', 1]]
        obj = ['max', 9, 5, 6, 4]
        s = bandb.BandB(number, cons, obj)
        s.solve(s.number, s.cons, s.obj, s.constant, [-1, -1, -1, -1])
        self.assertEqual(s.queue, {16.5: [[0, -1, -1, -1], [1, -1, -1, -1]]})

    def test_bandb(self):
        """
        max 9x1 + 5x2 + 6x3 + 4x4
        6x1 + 3x2 + 5x3 + 2x4 <= 10
                     x3 +  x4 <= 1
        -x1       +  x3       <= 0
              -x2       +  x4 <= 0
        0 <= x1, x2, x3, x4 <= 1
        the optimal value is 14
        and the solution is [1, 1, 0, 0]
        """
        number = 4
        cons = [[6, 3, 5, 2, '<=', 10],
                [0, 0, 1, 1, '<=', 1],
                [-1, 0, 1, 0, '<=', 0],
                [0, -1, 0, 1, '<=', 0],
                [1, 0, 0, 0, '>=', 0],
                [1, 0, 0, 0, '<=', 1],
                [0, 1, 0, 0, '>=', 0],
                [0, 1, 0, 0, '<=', 1],
                [0, 0, 1, 0, '>=', 0],
                [0, 0, 1, 0, '<=', 1],
                [0, 0, 0, 1, '>=', 0],
                [0, 0, 0, 1, '<=', 1]]
        obj = ['max', 9, 5, 6, 4]
        s = bandb.BandB(number, cons, obj)
        solution, opt = s.bandb()
        self.assertEqual(solution, [1, 1, 0, 0])
        self.assertEqual(opt, 14)

    def test_None(self):
        """
        max x1 + x2
        x1 + x2 <= 1
        x1 >= 0.5
        x2 >= 0.5
        0 <= x1, x2 <= 1
        """
        number = 2
        cons = [[1, 1, '<=', 1],
                [1, 0, '>=', 0.5],
                [0, 1, '>=', 0.5],
                [1, 0, '>=', 0],
                [1, 0, '<=', 1],
                [0, 1, '>=', 0],
                [0, 1, '<=', 1]]
        obj = ['max', 1, 1]
        s = bandb.BandB(number, cons, obj)
        solution, opt = s.bandb()
        self.assertEqual(solution, None)
        self.assertEqual(opt, None)

if __name__ == '__main__':
    main()
