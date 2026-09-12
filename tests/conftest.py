import yaml
from pathlib import Path
from pytest import fixture

from polaris.base.base_linter import DEFAULT_ENCODING, Linter, Conviction

class TestLinter(Linter):

    def _offense_code_fmt(self, conviction: Conviction):
        return conviction.offense_code

    def _severity_fmt(self, conviction: Conviction):
        return conviction.offense.severity.name 

@fixture(scope="package")
def get_test_linter():
    return TestLinter()

@fixture(scope="package")
def mock_scripts(request, tmp_path_factory):
    cfg_path =  Path(request.param).resolve()
    with open(cfg_path) as cfg_file:
        config = yaml.safe_load(cfg_file)

    dir = tmp_path_factory.mktemp(config["dir"])

    for file, content in config["files"].items():
        fpath = dir / file
        fpath.write_text(content, encoding=DEFAULT_ENCODING)

    return str(dir), dir

@fixture(scope="package")
def load_expected_lint_results(request):
    expec_result_path = Path(request.param).resolve()

    with open(expec_result_path, "r", encoding=DEFAULT_ENCODING) as expec_result_file:
        expec_result = yaml.safe_load(expec_result_file)

    return expec_result["sentence"]