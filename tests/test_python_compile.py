from django.test import TestCase
from OnlineCompilerPython.pycompiler.python_compile import check_code, \
                                                            make_safe_builtins


class MakeSafeBuiltinsClass(TestCase):

    def test_make_safe_builtins_open_check_positive(self):
        safe_builtins = make_safe_builtins()

        if "open" in safe_builtins:
            self.assert_(False)
        self.assert_(True)

    def test_make_safe_builtins_eval_check_positive(self):
        safe_builtins = make_safe_builtins()

        if "eval" in safe_builtins:
            self.assert_(False)
        self.assert_(True)

    def test_make_safe_builtins_exec_check_positive(self):
        safe_builtins = make_safe_builtins()

        if "exec" in safe_builtins:
            self.assert_(False)
        self.assert_(True)


class CheckCodeTestClass(TestCase):

    def test_check_code_import_os_raise_exception(self):
        input_code = "import os"
        try:
            check_code(input_code)
        except IOError as exc:
            if str(exc) == "Can't import os module":
                self.assert_(True)
        else:
            self.assert_(False)

    def test_check_code_exec_raise_exception(self):
        input_code = "exec(del sqlite3.db)"
        try:
            check_code(input_code)
        except Exception as exc:
            if str(exc) == "Can't use exec function":
                self.assert_(True)
        else:
            self.assert_(False)

    def test_check_code_without_exception(self):
        input_code = "l = [1,2,3]\nprint(l)"
        try:
            check_code(input_code)
        except Exception:
            self.assert_(False)
        else:
            self.assert_(True)
