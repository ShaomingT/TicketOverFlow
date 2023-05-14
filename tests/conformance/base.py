import unittest
import os


class BaseCase(unittest.TestCase):
    def host(self):
        base = os.environ.get('TEST_HOST', 'http://ticketoverflow-1558203388.us-east-1.elb.amazonaws.com/api/v1')
        if base[-1] == '/':
            return base[:-1]
        return base

    def assertDictSubset(self, expected_subset: dict, whole: dict):
        for key, value in expected_subset.items():
            if key not in whole:
                self.assertFalse(True, f'Key {key} not found in {whole}')
            if isinstance(value, dict):
                self.assertDictSubset(value, whole[key])
            self.assertEqual(value, whole[key])
