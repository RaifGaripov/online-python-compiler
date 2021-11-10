from multiprocessing import Process

from django.shortcuts import render
from OnlineCompilerPython.pycompiler.python_compile import make_safe_builtins,\
    check_code, execute_code

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
        runtime = int(request.POST["runtime"])
        output = ""

        try:
            # check in input_code for "import os"
            check_code(input_code)

            # make safe builtin to prevent usage of unsafe functions
            safe_builtins = make_safe_builtins()

            s_output = StringIO()

            # execution input code with safe_builtins limited by runtime

            with redirect_stdout(s_output):
                # start exec as Process
                code_execution = Process(target=exec,
                                         args=(input_code, safe_builtins,))
                code_execution.start()

                # wait until runtime is out
                code_execution.join(runtime)

                if code_execution.is_alive():
                    # if process still going terminate it
                    code_execution.terminate()

            # save stdout of executed code
            output = s_output.getvalue()

        except NameError as exc:
            # handle using not safe functions
            if exc.args[0] == "name 'open' is not defined":
                output = "Error: You can't use open function"
            if exc.args[0] == "name 'eval' is not defined":
                output = "Error: You can't use eval function"
            if exc.args[0] == "name 'exec' is not defined":
                output = "Error: You can't use exec function"

        except Exception as exc:
            # handle exceptions for returning theirs texts
            output = exc

        finally:
            # if got exception terminate code
            if code_execution.is_alive():
                code_execution.terminate()

            context = {
                "input_code": input_code,
                "output": output
            }

            return render(request, "index.html", context)
    else:
        return render(request, "index.html")
