import unittest
from test_calculator import Calculator

class CalculatorTestCase(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    def test_add(self):
        print("test_add",self.calc.add(5, 3))
        self.assertEqual(self.calc.add(1, 2), 3)
    def test_sub(self):
        print("test_sub",self.calc.subtract(
            10, 5))
        self.assertEqual(self.calc.subtract(2, 1), 1)
    def test_mul(self):
        print("test_mul",self.calc.multiply(
            2, 3))
        self.assertEqual(self.calc.multiply(2, 3), 6)
    def test_div(self):
        print("test_div",self.calc.divide(
            6, 2))
        self.assertEqual(self.calc.divide(6, 2), 4)

if __name__ == '__main__':
    unittest.main()