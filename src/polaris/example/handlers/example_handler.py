from pathlib import Path

from polaris.base.base_handler import BaseHandler

class ExampleHandler(BaseHandler):

    _SUFFIX     = ".py"
    _SPLITTER   = "_"

    def accept(self, file: Path) -> bool:
        has_suffix  = file.suffix == self._SUFFIX
        match_end   = file.stem.split(self._SPLITTER)[-1] == "example"

        if has_suffix and match_end:
            return True