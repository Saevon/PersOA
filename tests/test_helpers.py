from django.utils import unittest
from helpers import decorators

class Foo(object):
    """Class to test the cascade decorator"""
    def __init__(self):
        self.counter = 0

    @decorators.cascade
    def set_val(self, val):
        self.val = val
        self.counter += 1

    @decorators.cascade
    def count(self, val):
        self.counter = self.counter + val + 1

    def get_count(self):
        return self.counter

class TestCascade(unittest.TestCase):

    def setUp(self):
        self.foo = Foo()

    def test_cascade(self):
        out = (self.foo.set_val(3)
            .count(4)
            .count(5)
        )

        self.assertEqual(out, self.foo)
        self.assertEqual(out.get_count(), 12)
