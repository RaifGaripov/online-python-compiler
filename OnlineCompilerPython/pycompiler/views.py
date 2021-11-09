import sys

from django.shortcuts import render
from OnlineCompilerPython.pycompiler.python_compile import make_safe_builtins,\
                                                           check_code

from io import StringIO
from contextlib import redirect_stdout


def index(request):
    """Index Page"""
    return render(request, "index.html")


def runcode(request):
    """Execute python code from page and returns output of it,
    if exception was raised returns text of exception"""
    if request.method == "POST":
        input_code = request.POST["input"]
        output = ""

        try:
            # check in input_code for "import os"
            check_code(input_code)

            # make safe builtin to prevent usage of unsafe functions
            safe_builtins = make_safe_builtins()

            s_output = StringIO()

            # execution input code with safe_builtins
            with redirect_stdout(s_output):
                exec(input_code, {'__builtins__': safe_builtins}, None)

            # save stdout of executed code
            output = s_output.getvalue()

        except Exception as exc:
            # handle exceptions for returning theirs texts
            sys.stdout = sys.__stdout__
            output = exc

        finally:
            sys.stdout = sys.__stdout__
            context = {
                "input_code": input_code,
                "output": output
            }

            return render(request, "index.html", context)
    else:
        return render(request, "index.html")
