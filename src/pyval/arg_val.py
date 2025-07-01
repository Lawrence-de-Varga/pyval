import inspect
from typing import Callable
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
    NOTE: Only for use with positional arguments.
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

        def wrapper(*args):
            for idx, arg in enumerate(args):
                for val_func in arg_validation_funcs[idx]:
                    try:
                        if not val_func(arg):
                            raise ValueError
                    except ValueError:
                        raise ValueError(
                            f"Arg {idx} - '{param_names[idx]}' with the value: '{arg}', failed to satisfy '{val_func.__qualname__}'."
                        )
                    except Exception as e:
                        raise Exception(
                            f"arg_val_args failed while running '{val_func.__qualname__}' with the argument '{arg}' to '{func.__name__}': {e}."
                        )
            return func(*args)

        return wrapper

    return decorate


def arg_val_args_kwargs(arg_validation_funcs: dict[str : list[Callable]]):
    """
    Same as arg_val_args except it also operates of kwargs and it
    takes a dict as input where the keys are strings corresponding to the names of the
    parameters that are to be validated and the keys are lists of
    validation functions(predicate).
    NOTE: Currently is not able to validate default values for parameters so if they are checked
    they must be given values in the function call otherwise an error will be raised.
    """

    if not div.is_dict_of_val_funcs(arg_validation_funcs):
        raise TypeError(
            f"arg_validation_funcs must be a dict with paramaeter names as keys and lists of predicate functions as values, but got: {arg_validation_funcs}."
        )

    def decorate(func):
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())

        if len(arg_validation_funcs) == 0:
            raise ValueError(
                f"Redundant use of 'arg_val_args_kwargs'. Zero validation funtions provided to validate the arguments to '{func.__name__}'."
            )

        if len(arg_validation_funcs) > len(param_names):
            raise ValueError(
                f" The number of lists of validation functions: '{len(arg_validation_funcs)}', must not exceed the number of parameters to '{func.__name__}': '{len(param_names)}'."
            )

        def wrapper(*args, **kwargs):
            dargs = dict(zip(param_names, args))
            kwargs = dargs | kwargs

            for key in arg_validation_funcs.keys():
                if key not in kwargs:
                    raise LookupError(
                        f"'{key}' is not a parameter to '{func.__name__}'."
                    )

                for val_func in arg_validation_funcs[key]:
                    try:
                        if not val_func(kwargs[key]):
                            raise ValueError
                    except ValueError:
                        raise ValueError(
                            f"Arg '{key}' with the value: '{kwargs[key]}', failed to satisfy: '{val_func.__qualname__}'."
                        )
                    except Exception as e:
                        raise Exception(
                            f"arg_val_args_kwargs failed while running '{val_func.__qualname__}' with the argument: '{kwargs[key]}' to '{func.__name__}': {e}."
                        )
            return func(args)

        return wrapper

    return decorate
