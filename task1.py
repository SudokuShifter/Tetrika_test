import unittest

def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        for i, (arg, expected_type) in enumerate(annotations.items()):
            if not isinstance(args[i], expected_type):
                raise TypeError(f'{arg} must be {expected_type}')
        res = func(*args, **kwargs)
        return res
    return wrapper


@strict
def sum(a: int, b: int):
    return a + b


class Test(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum(1, 2), 3)
        self.assertRaises(TypeError, sum, 1, 2.15)
        self.assertRaises(TypeError, sum, 1, '2.15')
        self.assertEqual(sum(1, -2), -1)