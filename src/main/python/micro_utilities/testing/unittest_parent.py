import gzip
import json
import os
import random
import string
import unittest

PATH_TEMPLATE = "{base_path}/{resource_file}"


class ParentTestCase(unittest.TestCase):
    def tearDown(self):
        pass

    def assertEqual(self, first, second, msg=None):
        msg = "{msg} - actual: {first} expected: {second}".format(msg=msg, first=first, second=second)
        super(ParentTestCase, self).assertEqual(first, second, msg)

    @classmethod
    def setUpClass(cls):
        super(ParentTestCase, cls).setUpClass()
        cls.run_id = cls.randomWord(5)
        cls.resource_directory = None


    @classmethod
    def setUpResourceDirectory(cls,TEST_DIR):
        cls.resource_directory =  os.path.abspath(os.path.join(TEST_DIR, '../resources/'))

    @classmethod
    def randomWord(cls, param):
        return ''.join(random.choice(string.lowercase) for i in range(param))

    def setUp(self):
        super(ParentTestCase, self).setUp()


    @classmethod
    def _get_resource_path(cls, config):
        return os.path.join(cls.resource_directory, config)

    def open_resource_as_json(cls, resource_file, root_path=None):
        if not root_path:
            root_path = cls.resource_directory
        template_format = PATH_TEMPLATE.format(resource_file=resource_file, base_path=root_path)
        if ".gz" in resource_file:
            with gzip.open(template_format, "r") as fp:
                data = json.load(fp)
        else:
            with open(template_format, "r+") as fp:
                data = json.load(fp)
        return data

    def validate_exception(self, func_pointer, msg, kwargs=None):
        if not kwargs:
            kwargs = {}
        try:
            func_pointer(**kwargs)
            self.fail("Failed to throw exception for {}".format(msg))
        except:
            pass
