import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyval.type_check import type_check_args, type_check_args_strict


class TestTypeCheck(unittest.TestCase):
    def test_type_check_no_arg_types(self):
        with self.assertRaises(ValueError):

            @type_check_args([])
            def mul(x, y):
                return x * x

    def test_type_check_args_not_type_list(self):
        with self.assertRaises(TypeError):

            @type_check_args(["hello", 5, True])
            def mul(x, y):
                return x * y

    def test_type_check_args_too_many_types(self):
        with self.assertRaises(ValueError):

            @type_check_args([str, int, float, str])
            def mul(x, y):
                return x * y

            mul(7, 8)

    def test_type_check_ars_not_list(self):
        with self.assertRaises(TypeError):

            @type_check_args(str, list)
            def mul(x, y):
                return x * y
