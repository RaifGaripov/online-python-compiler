import re

from copy import deepcopy


def make_safe_builtins():
    """Copies __builtins__ list without open, exec, eval functions"""
    safe_builtins = deepcopy(globals().get("__builtins__"))

    not_safe_func = ["open", "exec", "eval"]
    for func in not_safe_func:
        del safe_builtins[func]

    return safe_builtins


def check_code(input_code):
    """Checks if input code meets the requirements, if doesn't raise exception:
    requirements of input code:
    doesn't import os module,
    doesn't contains open, exec, eval functions"""
    if re.search(r"import[\s\w\,({]*\bos", input_code) is not None:
        raise IOError("Can't import os module")
