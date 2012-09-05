from django.utils import unittest

from app.views.field import Field
from app.views.whitelist import Whitelist

class TestWhitelist(unittest.TestCase):

    def setUp(self):
        self.whitelist = Whitelist()

    def test_include(self):
        (self.whitelist
            .include(['test', 'inc_test'], 'inc_test')
            .include(['test2'], 'test2')
        )

        args = {
            'include': '["test"]'
        }

        out = self.whitelist.process(args)
        includes = out['include']
        out.pop('include')

        # The correct include keys
        self.assertTrue(includes['inc_test'])
        self.assertFalse(includes['test2'])

        # Make sure there are no keys in non-includes
        self.assertTrue(len(out) == 0)

    def test_include__empty(self):
        out = self.whitelist.process({})
        self.assertFalse(out.has_key('include'))

    def test_include__mixed(self):
        (self.whitelist
            .include(['test', 'inc_test'], 'inc_test')
            .include(['test', 'test2'], 'test2')
        )

        args = {
            'include': '["test"]',
        }

        out = self.whitelist.process(args)
        includes = out['include']
        out.pop('include')

        # The correct include keys
        self.assertTrue(includes['inc_test'])
        self.assertTrue(includes['test2'])


        self.assertTrue(len(out) == 0)

    @unittest.skip("TODO: Whitelists still need fix-up")
    def test_include__remove(self):
        (self.whitelist
            .include(['test', 'inc_test'], 'inc_test')
            .include(['test', 'test2'], 'test2')
            .remove('test2')
        )

        args = {
            'include': '["test"]',
        }

        out = self.whitelist.process(args)
        includes = out['include']

        # The correct include keys
        self.assertTrue(includes['inc_test'])
        self.assertFalse(includes.has_key('test2'))

        self.assertTrue(len(out) == 0)

    def test_require(self):
        (self.whitelist
            .require(Field(['test', 'name'], 'test', basestring))
        )

        args = {
            'test': 'The Test',
        }

        out = self.whitelist.process(args)

