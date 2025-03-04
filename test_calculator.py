# import unittest

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
    def multiply(self, a, b):
        return a * b
    def divide(self, a, b):
        return a / b

# class TestCalculator(unittest.TestCase):
    
#     def setUp(self):
#         self.calc = Calculator()

#     def test_add(self):
#         print("test_add",self.calc.add(5, 3))
#         self.assertEqual(self.calc.add(5, 3), 8)
#         self.assertEqual(self.calc.add(-1, 1), 0)

#     def test_subtract(self):
#         print("test_subtract",self.calc.subtract(10, 5))
#         self.assertEqual(self.calc.subtract(10, 5), 5)
#         self.assertEqual(self.calc.subtract(0, 5), -5)

# if __name__ == '__main__':
#     unittest.main()
