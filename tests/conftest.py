import json
from pathlib import Path
from pytest import fixture

from polaris.base.base_linter import DEFAULT_ENCODING

@fixture(scope="package")
def mock_scripts(request, tmp_path_factory):
    cfg_path =  Path(request.param).resolve()
    with open(cfg_path) as cfg_file:
        config = json.load(cfg_file)

    dir = tmp_path_factory.mktemp(config["dir"])

    for file, content in config["files"].items():
        fpath = dir / file
        fpath.write_text(content, encoding=DEFAULT_ENCODING)

    return str(dir), dir