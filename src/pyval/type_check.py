from . import decorator_input_validation as div


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
