import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyval.type_check import type_check_args, type_check_args_strict, type_check


class TestTypeCheck(unittest.TestCase):
    def test_type_check_no_hints(self):
        with self.assertRaises(ValueError):

            @type_check
            def mul(x, y):
                return x * y

    def test_type_check_bad_hints(self):
        with self.assertRaises(TypeError):

            @type_check
            def mul(x: 5, y: int):
                return x * y

    def test_type_check_wrong_types(self):
        with self.assertRaises(TypeError):

            @type_check
            def mul(x: int, y: float):
                return x * y

            mul("a", [1, 2, 3])

    def test_type_check_wrong_return_type(self):
        with self.assertRaises(TypeError):

            @type_check
            def mul(x, y) -> int:
                return (x, y)

            mul(9, 4)

    def test_type_check_returned_error(self):
        with self.assertRaises(Exception):

            @type_check
            def mul(x, y) -> int:
                raise Exception("Error")

            mul(9, 9)


class TestTypeCheckArgs(unittest.TestCase):
    def test_type_check_args_no_arg_types(self):
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

    def test_type_check_args_not_list(self):
        with self.assertRaises(TypeError):

            @type_check_args(str, list)
            def mul(x, y):
                return x * y

    def test_type_check_args_wrong_types(self):
        with self.assertRaises(TypeError):

            @type_check_args([str, list])
            def mul(x, y):
                return x * y

            mul(8, 9)

    def test_type_check_args_fewer_types(self):
        @type_check_args([int])
        def mul(x, y, z):
            return x * y * z

        self.assertEqual(mul(3, 4, 5), 60)


class TestTypeCheckArgsStrict(unittest.TestCase):
    def test_type_check_args_strict_isinstance(self):
        with self.assertRaises(TypeError):

            @type_check_args_strict([int])
            def obv(boolean):
                if boolean:
                    return True
                else:
                    return False

            obv(True)
