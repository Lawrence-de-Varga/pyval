from collections.abc import Callable


def is_type_list(type_list: list):
    if not isinstance(type_list, list):
        raise TypeError(f"is_type_list requires a list of types but got: '{type_list}'")
    return all(isinstance(item, type) for item in type_list)


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
