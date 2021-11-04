import sys

from django.shortcuts import render

# Create your views here.


def index(request):
    """Index Page"""
    return render(request, "index.html")


def runcode(request):
    """Execute python code from page and returns output of it"""
    if request.method == "POST":
        input_code = request.POST["input"]
        output = ""

        try:
            sys.stdout = open("file.txt", "w")

            exec(input_code)

            sys.stdout.close()

            with open("file.txt", "r") as ou_f:
                output_lines = []
                for line in ou_f:
                    output_lines.append(line)
                output = "".join(output_lines)

        except Exception as exc:
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
