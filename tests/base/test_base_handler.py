from pathlib import Path

from pytest import mark

from polaris.base.base_handler import BaseHandler

@mark.base
@mark.base_handler
class TestHandler(BaseHandler):

    def accept(self, file: Path) -> bool:
        if file.suffix == ".py":
            return True

    @mark.base
    @mark.base_handler
    @mark.parametrize(
        "mock_scripts",
        ["tests/base/test_base_handler.json"],
        indirect=True
    )
    def test_collect(self, mock_scripts):
        dir_str, _  = mock_scripts
        dir_list    = [dir_str]
        want        = 2
        got         = 0

        for _ in self.collect(dir_list):
            got += 1

        assert got == want
