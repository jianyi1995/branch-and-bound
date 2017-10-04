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

if __name__ == '__main__':
    main()