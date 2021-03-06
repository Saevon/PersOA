from app.views.field import Field, FieldError

import unittest


class TestFields(unittest.TestCase):

    def setUp(self):
        self.field = Field(['in'], 'out')

    def test_type_checker(self):
        is_int = Field.type_checker(int)
        self.assertTrue(is_int(1), 'int type checker fails')
        self.assertTrue(is_int(1), 'getting another int type checker fails')

    def test_type_checker__subclass(self):
        is_str = Field.type_checker(str)
        self.assertFalse(is_str(u'sample'))
        is_basestr = Field.type_checker(basestring)
        self.assertTrue(is_basestr(u'sample'))

    def test_type_checker__custom_types(self):
        Cls = type('Cls', (object,), {})
        is_Cls = Field.type_checker(Cls)

        self.assertTrue(is_Cls(Cls()))
        self.assertFalse(is_Cls(1))

        Cls2 = type('Cls2', (Cls,), {})
        is_Cls2 = Field.type_checker(Cls)

        self.assertTrue(is_Cls2(Cls2()))
        self.assertTrue(is_Cls2(Cls()))
        self.assertFalse(is_Cls2(1))

    def test_validation__new_validator(self):
        self.field.validator(lambda val: ((int(val) - 1) % 5))

        val = "16"
        self.assertFalse(self.field._validate_val(val))

    def test_basic(self):
        params = {'in': '"sample"',}

        val = self.field.val(params)
        self.assertEquals(val, 'sample')

    def test_multiple_keys(self):
        params = {'in': '1',}

        self.field = Field(['more', 'in'], 'name', int)

        val = self.field.val(params)
        self.assertEquals(val, 1)

    def test_multiple_keys__both_found(self):
        # TODO: This acts strange since sets sort their keys weirdly
        params = {
            'in': '1',
            'more': '2',
        }

        self.field = Field(['more', 'in'], 'name', int)
        val = self.field.val(params)
        # The item should be the last key that was passed in
        self.assertEquals(val, 1, 'Key Priority is wrong')

        self.field = Field(['in', 'more'], 'name', int)
        val = self.field.val(params)
        # The item should be the first key that was passed in
        self.assertEquals(val, 2, 'Key Priority is wrong')

    def test_add_key(self):
        params = {
            'one': '"1"',
            'two': '"2"',
            'three': '"3"',
        }

        self.field.key('two')
        val = self.field.val(params)
        self.assertEquals(val, '2')

    def test_not_found_items(self):
        with self.assertRaises(FieldError):
            params = {'none': '"sample"'}

            val = self.field.val(params)

    def test_default(self):
        params = {'none': '"sample"',}

        self.field.default('Not Found')
        val = self.field.val(params)
        self.assertEquals(val, 'Not Found')

    def test_default__error(self):
        params = {}

        # Make sure that exceptions are thrown
        Fail = FieldError
        self.field.default(Fail)
        with self.assertRaises(Fail):
            val = self.field.val(params)

        # make sure that indirect subclasses of BaseException are still thrown
        class Fail2(FieldError):
            pass

        self.field.default(Fail2)
        with self.assertRaises(Fail2):
            val = self.field.val(params)

    def test_default__twice(self):
        params = {'none': '"sample"',}

        self.field.default('Not Found').default('Fail')
        val = self.field.val(params)
        self.assertEquals(val, 'Fail')

    def test_get_name(self):
        self.assertEquals(self.field.get_name(), 'out')

    def test_setting_list(self):
        params = {
            'sample': '["1","2"]',
            'in': '["1","2"]',
        }

        self.field.setting(Field.SETTINGS_LIST)
        val = self.field.val(params)
        self.assertItemsEqual(val, ["1","2"])

    def test_setting_limit__not_found(self):
        params = {'in': '"sample"',}

        (self.field.default('Fail')
            .setting(Field.SETTINGS_LIMIT)
        )
        val = self.field.val(params)
        self.assertEquals(val, 'Fail')

    def test_setting_limit__explicit(self):
        (self.field.setting(Field.SETTINGS_LIMIT)
            .choice('allowed item')
        )

        params = {'in': '"allowed item"',}

        val = self.field.val(params)
        self.assertEquals(val, 'allowed item')

        params = {'in': '"not allowed"'}
        with self.assertRaises(FieldError):
            val = self.field.val(params)

    def test_setting_limit_implicit(self):
        self.field.choice('allowed item')

        params = {'in': '"allowed item"',}

        val = self.field.val(params)
        self.assertEquals(val, 'allowed item')

        params = {'in': '"not allowed"'}
        with self.assertRaises(FieldError):
            val = self.field.val(params)

    def test_setting_limit_implicit_chain(self):
        (self.field.choice('allowed item')
            .choice('other item')
            .choice('final item')
        )

        # check the third one to ensure that:
        # a) the first call doesn't cause others to fail
        # b) the choice isn't overwritten, but all of them are kept
        params = {'in': '"other item"',}

        val = self.field.val(params)
        self.assertEquals(val, 'other item')

        params = {'in': 'not allowed'}
        with self.assertRaises(FieldError):
            val = self.field.val(params)

    def test_setting_limit_list(self):
        (self.field.choice('allowed item')
            .choice('other item')
            .choice('final item')
            .setting(Field.SETTINGS_LIST)
        )

        params = {
            'in': '["other item", "final item", "other item", "allowed item"]',
        }

        val = self.field.val(params)
        self.assertItemsEqual(
            val,
            ['other item', 'final item', 'other item', 'allowed item']
        )

        params = {'in': '"not allowed"'}
        with self.assertRaises(FieldError):
            val = self.field.val(params)

    def test_setting_limit_list__empty(self):
        (self.field.choice('allowed item')
            .choice('other item')
            .choice('final item')
            .setting(Field.SETTINGS_LIST)
        )

        params = {
            'in': '[]',
        }

        val = self.field.val(params)
        self.assertItemsEqual(
            val,
            []
        )


    def test_setting_limit_list__filtered_items(self):
        '''
        Sometimes you want to filter out values that are invalid, but allow the rest
        '''
        (self.field.choice('allowed item')
            .choice('other item')
            .choice('final item')
            .setting(Field.SETTINGS_LIST)
            .setting(Field.SETTINGS_LIST_FILTERED)
        )

        params = {
            'in': '["other item", "final item", "fail item"]',
        }

        val = self.field.val(params)
        self.assertItemsEqual(
            val,
            ['other item', 'final item'],
        )

    def test_setting_limit_list__filtered_items__none_pass(self):
        (self.field.choice('allowed item')
            .choice('other item')
            .choice('final item')
            .setting(Field.SETTINGS_LIST)
            .setting(Field.SETTINGS_LIST_FILTERED)
        )

        params = {
            'in': '["Fail", "More Fail", "fail item"]',
        }
        val = self.field.val(params)
        self.assertItemsEqual(
            val,
            []
        )


    def test_setting_limit_list__filtered_items__non_empty(self):
        (self.field.choice('allowed item')
            .choice('other item')
            .choice('final item')
            .setting(Field.SETTINGS_LIST)
            .setting(Field.SETTINGS_LIST_FILTERED)
            .setting(Field.SETTINGS_LIST_NON_EMPTY)
        )

        params = {
            'in': '["Fail", "More Fail", "fail item"]',
        }

        with self.assertRaises(FieldError):
            val = self.field.val(params)

