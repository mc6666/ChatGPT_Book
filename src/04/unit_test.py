def sum_numbers(a, b):
    return a + b

import unittest

class TestSumNumbers(unittest.TestCase):

    def test_sum_numbers(self):
        self.assertEqual(sum_numbers(1, 2), 3)
        self.assertEqual(sum_numbers(-1, 1), 0)
        self.assertEqual(sum_numbers(0, 0), 0)

if __name__ == '__main__':        
    unittest.main()  