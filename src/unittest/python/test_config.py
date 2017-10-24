import os
import unittest

import micro_utilities.testing.test_flask_app
from micro_utilities.config import ConfigManager
from micro_utilities.testing import test_flask_app
from micro_utilities.testing.unittest_parent import ParentTestCase


class TestConfigurationManager(ParentTestCase):
    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        ConfigManager.config = None
        del os.environ[ConfigManager.CONFIG_FILE]

    @classmethod
    def setUpClass(cls):
        super(TestConfigurationManager, cls).setUpClass()
        cls.setUpResourceDirectory(os.path.dirname(os.path.abspath(__file__)))
        ConfigManager.config = None
        os.environ[ConfigManager.CONFIG_FILE] = cls._get_resource_path('test_config/test_config.json')

    def test_config_load(self):
        os.environ['ENVIRONMENT'] = 'unit_test'
        print "\nConfig:"
        print os.environ[ConfigManager.CONFIG_FILE]
        self.assertEqual(ConfigManager.get_value("foo"), 'default-foo',
                         "Did not load default value for foo - {}".format(ConfigManager.get_value("foo")))
        self.assertEqual(ConfigManager.get_value("bar"), 'default-foo-bar', "Did not substitute value for bar")
        self.assertEqual(ConfigManager.get_value("baz"), 'unit-test-baz',
                         "Did not override environmental value value for baz")
        self.assertEqual(ConfigManager.get_value("baz"), 'unit-test-baz',
                         "Did not override environmental value value for baz")
        self.assertEqual(ConfigManager.get_secret("baz"), 'unit-test-baz',
                         "Did not get secret")
        self.assertEqual(ConfigManager.get_int_value("my-number"), 3, "Did not load 3 as expected")
        self.assertEqual(ConfigManager.get_boolean("my-bool"), True, "Did not load true as expected")
        self.assertEqual(os.environ["AWS_SECRET_ACCESS_KEY"], 'secret-key', "Did not find aws secret in environment")
        self.assertEqual(os.environ["AWS_ACCESS_KEY_ID"], 'key', "Did not find aws key id in environment")

    def test_flask_init(self):
        ConfigManager.init_flask_app(test_flask_app.app)
        ConfigManager.init_flask_logging(test_flask_app.app)
        self.assertEqual(test_flask_app.app.config['AWS_ACCESS_KEY_ID'],'key',"Did not init app")
