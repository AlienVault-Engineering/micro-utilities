import os

from micro_utilities.http import session_factory
from micro_utilities.testing.unittest_parent import ParentTestCase


class TestParentManager(ParentTestCase):
    def setUp(self):
        pass


    @classmethod
    def setUpClass(cls):
        super(TestParentManager, cls).setUpClass()
        cls.setUpResourceDirectory(os.path.dirname(os.path.abspath(__file__)))

    def test_random_word(self):
        self.assertNotEqual(self.randomWord(5),self.randomWord(5),"not random")

    def test_json_load(self):
        self.assertEqual(self.open_resource_as_json("test_parent/test.json"),{"foo":"bar"},"not loaded")
