from app.views.cases import IncludeCase
from django.utils import unittest

class IncludeCaseTest(unittest.TestCase):
    def setUp(self):
        self.case = IncludeCase(['data'])

    def test_basic(self):
        params = {
            'name': 'sample',
            'include': ['stuff', 'data'],
        }

        self.assertTrue(self.case.passed(params))

    def test_not_found(self):
        params = {
            'name': 'sample',
            'include': ['stuff', 'other'],
        }

        self.assertFalse(self.case.passed(params))

    def test_no_includes(self):
        """
        Make sure that it doesn't break if there are no includes
        """
        params = {
            'name': 'sample',
            'include': [],
        }

        #empty lists don't break
        self.assertFalse(self.case.passed(params))

        params = {
            'name': 'sample',
        }

        # Not having the key at all doesn't break it either
        self.assertFalse(self.case.passed(params))

    def test_multiple_keys(self):
        params = {
            'name': 'sample',
            'include': ['data', 'other', 'stuff'],
        }
        self.case.key('stuff')

        self.assertTrue(self.case.passed(params))

    def test_multiple_keys__not_all_found(self):
        params = {
            'name': 'sample',
            'include': ['data', 'other', 'stuff'],
        }
        self.case.key('not found')

        self.assertFalse(self.case.passed(params))
