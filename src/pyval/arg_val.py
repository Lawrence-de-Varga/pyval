import inspect
from functools import wraps
from pathlib import Path
from collections.abc import Callable
from . import decorator_input_validation as div


def arg_val_args(arg_validation_funcs: list[list[Callable]]):
    """
    Takes a list of lists of predicate validation functions. Each list of functions
    should correspond by index to one positional argument in the decorated function.
    Each validation function in a particular list is called on the corresponding positional argument.
    If any validation function returns False, an error is raised.
    If the number of lists of validation functions is less than the
    number of positional arguments to the decorated function
    only the first n parameters are validated, where n is the number of
    lists of validation functions provided.
    If more are provided, an error is raised.
    """

    if not div.is_list_of_list_of_funcs(arg_validation_funcs):
        raise TypeError(
            f"arg_validation_funcs must be a list of lists of predicate functions, but contains: {arg_validation_funcs}."
        )

    def decorate(func):
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())

        if len(arg_validation_funcs) == 0:
            raise ValueError(
                f"Redundant use of 'arg_val_args'. Zero validation funtions provided to validate the arguments to '{func.__name__}'."
            )

        if len(arg_validation_funcs) > len(param_names):
            raise ValueError(
                f" The number of lists of validation functions: '{len(arg_validation_funcs)}', must not exceed the number of parameters to '{func.__name__}': '{len(param_names)}'."
            )

        @wraps(func)
        def wrapper(*args):
            idx = 0
            for arg in args:
                for val_func in arg_validation_funcs[idx]:
                    if not val_func(arg):
                        raise ValueError(
                            f"Arg {idx} - {param_names[idx]}: '{args[idx]}', failed to satisfy '{val_func.__name__}'."
                        )
                idx += 1
            return func(*args)

        return wrapper

    return decorate
