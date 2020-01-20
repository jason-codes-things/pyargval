# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 20:13:23 2019

@author: Jason G
"""

import functools
import inspect

from utilities.bool_ops import ordnumfalse


def inputargtypes(*accepted_arg_types, **accepted_kwarg_types):
    # A decorator to validate input parameter types of a given function.

    def accept_decorator(validate_function):
        # Check if the positional and keyword arguments match the accepted
        # types as specified by accepted_art_types and accepted_kwarg_types
        # respectively.

        @functools.wraps(validate_function)
        def decorator_wrapper(*input_args, **input_kwargs):
            func_sig = inspect.signature(validate_function)     # Allows us to read paired keywords and defaults.
            kwarg_isvalid = [type(func_sig.parameters[key].default) == type(val) for key, val in
                             zip(input_kwargs.keys(), input_kwargs.values())]

            input_arg_types = [type(value) for value in input_args[1:]]
            arg_isvalid     = list(map(arg_compare, range(len(accepted_arg_types)), input_arg_types))

            ordnum_arg_notvalid   = ordnumfalse(arg_isvalid)
            ordnum_kwarg_notvalid = ordnumfalse(kwarg_isvalid)
            keys_kwarg_notvalid   = [list(input_kwargs.keys())[i] for i in ordnum_kwarg_notvalid]

            if len(ordnum_arg_notvalid) != 0:
                raise AssertionError(
                    ArgumentValidationError(ordnum_arg_notvalid,
                                            input_args[0].__class__.__name__,
                                            [accepted_arg_types[i] for i in ordnum_arg_notvalid]))

            if len(ordnum_kwarg_notvalid) != 0:
                raise AssertionError(
                    ArgumentValidationError(ordnum_kwarg_notvalid,
                                            input_args[0].__class__.__name__,
                                            [accepted_kwarg_types[key] for key in keys_kwarg_notvalid],
                                            'keyword argument'))

            return validate_function(*input_args, **input_kwargs)
        return decorator_wrapper

    def arg_compare(iarg, argtype):
        return accepted_arg_types[iarg] == argtype

    return accept_decorator


class ArgumentValidationError(ValueError):
    # Raised when the type of an argument to a function is not what it should be.

    def __init__(self, arg_num, func_name, accepted_arg_type, input_type='positional argument'):
        self.error = ''.join(['\nThe {0} {1}(s) of {2}() is not a {3}.'.format(
                        x,input_type,func_name,y) for i, (x,y) in enumerate(zip(arg_num,accepted_arg_type))])

    def __str__(self):
        return self.error

