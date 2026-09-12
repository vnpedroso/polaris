from pytest import mark 

from polaris.base.base_linter import Lint

from polaris.example.handlers.example_handler import ExampleHandler

from polaris.example.checkers.unused_variable import UnusedVarChecker

@mark.linter
@mark.example
@mark.parametrize(
    "mock_scripts",
    ["tests/example/linter/test_example_linter.yaml"],
    indirect=True
)
@mark.parametrize(
    "load_expected_lint_results",
    ["tests/example/linter/test_example_linter_expected.yaml"],
    indirect=True
)
def test_example_lint(mock_scripts, get_test_linter, load_expected_lint_results, capsys):

    dir_str, _  = mock_scripts
    dir_list    = [dir_str]

    handler     = ExampleHandler()

    linter      =   get_test_linter

    linter.checkers.add(UnusedVarChecker(offense_code="TEST_EXP_001"))

    exit_code   =   Lint(linter,handler,dir_list)
    stdout      =   capsys.readouterr().out

    got      =   set(stdout.splitlines())
    want     =   set(load_expected_lint_results.splitlines())

    assert got          == want
    assert exit_code    ==  0 