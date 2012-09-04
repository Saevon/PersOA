from django.utils import unittest
from utils import decorators

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

    def test_basic(self):
        out = (self.foo.set_val(3)
            .count(4)
            .count(5)
        )

        self.assertEqual(out, self.foo)
        self.assertEqual(out.get_count(), 12)


def add_one(dictionary, field):
    dictionary[field] += 1

class TestAllowList(unittest.TestCase):

    def setUp(self):
        self.params = {'main': 0, 'sec': 0}
        self.attr = {'main': 0, 'sec': 0}

    def test_pos_arg__single(self):
        func = decorators.allow_list(1)(add_one)

        func(self.attr, 'main')
        self.assertEquals(self.attr['main'], 1)

        func = decorators.allow_list(0)(add_one)

        func(self.attr, 'sec')
        self.assertEquals(self.attr['sec'], 1)
        func(self.params, 'main')
        self.assertEquals(self.params['main'], 1)

    def test_pos_arg__list(self):
        func = decorators.allow_list(1)(add_one)

        func(self.attr, ['main', 'sec', 'main'])
        self.assertEquals(self.attr['main'], 2)
        self.assertEquals(self.attr['sec'], 1)

    def test_key_arg__single(self):
        func = decorators.allow_list(1, 'field')(add_one)

        func(self.attr, 'main')
        self.assertEquals(self.attr['main'], 1)
        func(self.attr, field='main')
        self.assertEquals(self.attr['main'], 2)

    def test_key_arg__list(self):
        func = decorators.allow_list(1, 'field')(add_one)

        func(self.attr, ['main', 'sec', 'main'])
        self.assertEquals(self.attr['main'], 2)
        self.assertEquals(self.attr['sec'], 1)
        func(self.attr, field=['main', 'sec', 'main'])
        self.assertEquals(self.attr['main'], 4)
        self.assertEquals(self.attr['sec'], 2)
