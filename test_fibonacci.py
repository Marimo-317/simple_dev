import unittest
from fibonacci import fibonacci


class TestFibonacci(unittest.TestCase):
    """Test cases for the fibonacci function."""
    
    def test_fibonacci_zero(self):
        """Test fibonacci(0) returns empty list."""
        result = fibonacci(0)
        self.assertEqual(result, [])
    
    def test_fibonacci_one(self):
        """Test fibonacci(1) returns [0]."""
        result = fibonacci(1)
        self.assertEqual(result, [0])
    
    def test_fibonacci_two(self):
        """Test fibonacci(2) returns [0, 1]."""
        result = fibonacci(2)
        self.assertEqual(result, [0, 1])
    
    def test_fibonacci_five(self):
        """Test fibonacci(5) returns correct sequence."""
        result = fibonacci(5)
        expected = [0, 1, 1, 2, 3]
        self.assertEqual(result, expected)
    
    def test_fibonacci_ten(self):
        """Test fibonacci(10) returns correct sequence."""
        result = fibonacci(10)
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.assertEqual(result, expected)
    
    def test_fibonacci_negative(self):
        """Test fibonacci with negative input raises ValueError."""
        with self.assertRaises(ValueError):
            fibonacci(-1)
    
    def test_fibonacci_large(self):
        """Test fibonacci with larger input."""
        result = fibonacci(15)
        self.assertEqual(len(result), 15)
        # Check last few numbers
        self.assertEqual(result[-1], 377)  # 15th Fibonacci number
        self.assertEqual(result[-2], 233)  # 14th Fibonacci number


if __name__ == "__main__":
    unittest.main()
