import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyval.type_check import type_check_args, type_check_args_strict


class TestTypeCheck(unittest.TestCase):
    def test_type_check_no_arg_types(self):
        @type_check_args([])
        def mul(x, y):
            return x * x

        self.assertRaises(ValueError)

    def test_type_check_args_not_type_list(self):
        @type_check_args(["hello", 5, True])
        def mul(x, y):
            return x * y

        self.assertRaises(TypeError)
