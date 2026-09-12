import sys

from polaris.base.base_linter import Linter, Lint
from polaris.example.handlers.example_handler import ExampleHandler
from polaris.example.checkers.unused_variable import UnusedVarChecker

def example_lint():

    handler     = ExampleHandler()
    linter      = Linter()

    linter.checkers.add(UnusedVarChecker(offense_code="EXP_001"))

    exit_code = Lint(linter, handler)

    sys.exit(exit_code)