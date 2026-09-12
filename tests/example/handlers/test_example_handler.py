from pytest import mark

from polaris.example.handlers.example_handler import ExampleHandler

@mark.handler
@mark.example
class TestExampleHandler(ExampleHandler):

    @mark.parametrize(
        "mock_scripts",
        ["tests/example/handlers/test_example_handler.yaml"],
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