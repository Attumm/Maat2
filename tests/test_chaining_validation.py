import os
import sys
import unittest

import maat
from maat import registered_functions, chain_validation, Invalid


@chain_validation(registered_functions['str']) 
def valid_filename(val, extensions=('jpg',)):
    """Validates a filename extension and returns the 'str' validated value.

    Raises:
        Invalid: invalid filename extension
    """
    if not '.' in val or val.split('.')[-1].lower() not in extensions:
        raise Invalid('filename {} has an invalid extension'.format(val))
    return val 


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class TestEncryptDecrypt(unittest.TestCase):
    """For eu compliance reasons data user data is stored encrypted in
    the database. Following examples take the stated above as true.
    Don't use the encryption that is used in this example in production."""
    def setUp(self):
        self.expected = {
            'name': 'John Doe',
            'address': 'John Doe Street',
        }

        self.expected_encoded = {
            'name': 'LcyInWDZsUv22ocRHM3+yg7QO9ArjlhP2R9v5CSZIRc=',
            'address': 'LcyInWDZsUv22ocRHM3+yryn2OYg2jesvpgClxA/sdQ=',
        }


    def test_validate_and_transform_incoming_data(self):
        """This test takes data, validates and then encrypt"""
        test_input = {
            'name': 'John Doe',
            'address': 'John Doe Street',
        }
        counter_dict = {
            'name': {
                'validator': 'str', 'regex': 'John Doe', 'transform': 'encode'
            },
            'address': {
                'validator': 'str', 'regex': 'John Doe Street', 'transform': 'encode'
            },
        }
        validated_items = maat.scale(test_input, counter_dict)
        difference = ddiff(validated_items, self.expected_encoded)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})
