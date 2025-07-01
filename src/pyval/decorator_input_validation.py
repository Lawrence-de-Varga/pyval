from typing import Callable


def is_type_list(type_list: list):
    if not isinstance(type_list, list):
        raise TypeError(
            f"is_type_list requires a list of types but got: '{type(type_list)}'"
        )
    return all(isinstance(item, type) for item in type_list)


def values_are_types(type_dict: dict) -> bool:
    if not isinstance(type_dict, dict):
        raise TypeError(
            f"'items_are_types' requires a dict whose values are types but got: '{type(type_dict)}'"
        )
    return is_type_list(list(type_dict.values()))


def is_list_of_list_of_funcs(llf: list[list[Callable]]):
    if not isinstance(llf, list):
        raise TypeError(
            f"is_type_list requires a list of lists of predicate functions but got: '{llf}'"
        )
    if not all(isinstance(item, list) for item in llf):
        return False

    for f_list in llf:
        if not all(isinstance(item, Callable) for item in f_list):
            return False
    return True


def is_dict_of_val_funcs(func_dict: dict) -> bool:
    if not isinstance(func_dict, dict):
        raise TypeError(
            f"'is_dict_of_val_funcs' takes a 'dict' as an argument but got'{func_dict}' of type '{type(func_dict)}'."
        )

    if not all(isinstance(key, str) for key in func_dict.keys()):
        raise ValueError(f"func_dict must have strings as keys.")

    return is_list_of_list_of_funcs(list(func_dict.values()))
