import os

from micro_utilities.http import session_factory
from micro_utilities.testing.unittest_parent import ParentTestCase


class TestSessionManager(ParentTestCase):
    def setUp(self):
        pass


    @classmethod
    def setUpClass(cls):
        super(TestSessionManager, cls).setUpClass()
        cls.setUpResourceDirectory(os.path.dirname(os.path.abspath(__file__)))

    def test_session_manager(self):
        self.assertIsNotNone(session_factory.session(),"Session factory in fact factored a session")
