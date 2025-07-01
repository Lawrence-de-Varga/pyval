import inspect
from typing import get_type_hints, Callable
from . import decorator_input_validation as div


def type_check(func):
    """
    Checks the types passed to and returned from the decorated function against any type hints
    supplied(If there are none it throws an error).
    NOTE: Uses isinstance to compare types so bool will be an int etc. use type_check_strict
    if stricter checks are required.
    NOTE: coes not check the type of default values of parameters, so if they are wrong the problem will not be caught.
    """
    if not isinstance(func, Callable):
        raise TypeError(
            f"'{func}' must be an instance of 'Callable' but is of type: '{type(func)}'."
        )

    type_hints = get_type_hints(func)

    if len(type_hints) == 0:
        raise ValueError(
            f"Redundant use of 'type_check'. Zero type hints provided to check the arguments to '{func.__name__}'"
        )

    if not div.values_are_types(type_hints):
        raise TypeError(
            f"type hints contain undefined types or non-type objects: {type_hints}."
        )

    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())

        for idx, arg in enumerate(args):
            arg_type = type(arg)
            param_type = type_hints.get(param_names[idx], None)
            if param_type is None:
                continue
            if not isinstance(arg, param_type):
                raise TypeError(
                    f"'{param_names[idx]}' should be of type: '{param_type}', but is of type: '{arg_type}'."
                )

        for key, val in kwargs.items():
            arg_type = type(val)
            param_type = type_hints.get(key, None)
            if param_type is None:
                continue
            if not isinstance(val, param_type):
                raise TypeError(
                    f"'{key}' should be of type: '{param_type}', but is of type: '{arg_type}'."
                )

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            raise Exception(f"Error: '{func.__name__}' has failed with error: '{e}'.")

        if "return" in type_hints:
            if not isinstance(result, type_hints["return"]):
                raise TypeError(
                    f"'{func.__name__}' has a return type of: '{type_hints['return']}' but returned a value of type: '{type(result)}'."
                )
        return result

    return wrapper


def type_check_args(arg_types: list):
    """
    Check the types of the arguments passed to the
    decorated function. The arg_types list should contain
    the type names (e.g. str, int, float, etc) in the same order
    as the corresponding arguements are passed to the
    decorated function. If fewer types are provided
    than the number of arguments passed, only the first
    n arguments will be checked, where n is the number of types passed.
    """
    if not div.is_type_list(arg_types):
        raise TypeError(
            f"arg_types must contain only types, but contains: {arg_types}."
        )

    def decorate(func):
        if len(arg_types) == 0:
            raise ValueError(
                f"Redundant use of 'type_check_args'. Zero types provided to check the arguments to '{func.__name__}'."
            )

        def wrapper(*args):
            print("executing wrapper")
            if len(arg_types) > len(args):
                raise ValueError(
                    f"The number of types to check: {len(arg_types)}, must not exceed the number of parrameters to {func.__name__}: {len(args)}."
                )

            idx = 0
            for arg_type in arg_types:
                if not isinstance(args[idx], arg_types[idx]):
                    raise TypeError(
                        f"Arg {idx} : '{args[idx]}' to '{func.__name__}' must be of type: '{arg_types[idx]}' but is of type: '{type(args[idx])}'"
                    )
                idx += 1

            return func(*args)

        return wrapper

    return decorate


def type_check_args_strict(arg_types: list):
    """
    Check the types of the arguments passed to the
    decorated function. The arg_types list should contain
    the type names (e.g. str, int, float, etc) in the same order
    as the corresponding arguements are passed to the
    decorated function. If fewer types are provided
    than the number of arguments passed, only the first
    n arguments will be checked, where n is the number of types passed.
    This is the 'strict' version which does not consider subclasses
    as equal to super classes. I.e it does not check with
    isInstance().
    """

    if not div.is_type_list(arg_types):
        raise ValueError(
            f"arg_types must contain only types, but contains: {arg_types}."
        )

    def decorate(func):
        if len(arg_types) == 0:
            raise ValueError(
                f"Redundant use of 'type_check_args_strict'. Zero types provided to check the arguments to '{func.__name__}'."
            )

        def wrapper(*args):
            if len(arg_types) > len(args):
                raise ValueError(
                    f"The number of types to check: {len(arg_types)}, must not exceed the number of parrameters to {func.__name__}: {len(args)}."
                )

            idx = 0
            for arg_type in arg_types:
                if type(args[idx]) != arg_types[idx]:  # noqa: E721
                    raise TypeError(
                        f"Arg {idx} : '{args[idx]}' to '{func.__name__}' must be of type: '{arg_types[idx]}' but is of type: '{type(args[idx])}'"
                    )
                idx += 1
            return func(*args)

        return wrapper

    return decorate
