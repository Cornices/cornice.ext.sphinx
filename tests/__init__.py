# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import mock
from unittest import TestCase

from pyramid import testing as pyramid_testing

from cornice_sphinx import rst2html, ServiceDirective


class TestUtil(TestCase):

    def test_rendering(self):
        text = '**simple render**'
        res = rst2html(text)
        self.assertEqual(res, b'<p><strong>simple render</strong></p>')
        self.assertEqual(rst2html(''), '')

    def test_from_json_to_dict(self):
        from cornice_sphinx import from_json_to_dict

        argument = '{"user": "customer", "data": "information"}'
        self.assertEqual(
            from_json_to_dict(argument),
            {'user': 'customer', 'data': 'information'},
        )


class TestServiceDirective(TestCase):

    def setUp(self):
        super(TestServiceDirective, self).setUp()
        config = pyramid_testing.setUp()

        def Configurator(settings):
            return config

        # We need to mock the Configurator, otherwise each test uses the global registry to create
        # test resources. This leads to an error with Cornice >= 1.4, where resources conflicts
        # became an error.
        self.config_patch = mock.patch('tests.dummy.Configurator', Configurator)
        self.config_patch.start()
        param = mock.Mock()
        param.document.settings.env.new_serialno.return_value = 1

        self.directive = ServiceDirective(
            'test', [], {}, [], 1, 1, 'test', param, 1)
        self.directive.options['app'] = 'tests.dummy'
        self.directive.options['services'] = ['users', "thing_service"]

    def tearDown(self):
        self.config_patch.stop()
        pyramid_testing.tearDown()
        super(TestServiceDirective, self).tearDown()

    def test_module_reload(self):
        self.directive.options['app'] = None
        self.directive.options['services'] = None
        self.directive.options['modules'] = ['cornice']
        ret = self.directive.run()
        self.assertEqual(ret, [])

    def test_dummy(self):
        ret = self.directive.run()
        self.assertEqual(len(ret), 2)
        self.assertIn('Users service at', str(ret[0]))
        self.assertIn('Thing_Service service at ', str(ret[1]))

    def test_string_validator_resolved(self):
        # A validator defined as a string should be parsed as an obj,
        # ensuring the docstring contains validator.__doc__ rather
        # than str.__doc__.
        ret = self.directive.run()
        self.assertNotIn("str(object='') -> string", str(ret[0]))

    def test_docstring_replace(self):
        self.directive.options['docstring-replace'] = {
            'user': 'customer', 'data': 'information'}
        ret = self.directive.run()
        self.assertIn('Returns the customer information', str(ret[0]))
