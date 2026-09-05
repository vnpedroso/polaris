from pathlib import Path
from abc import ABC, abstractmethod

class BaseHandler(ABC):

    @abstractmethod
    def accept(self, path: Path) -> bool:
        pass 

    def collect(self, files: list[str]):
        for file in files:
            path = Path(file)

            # path object is either a file or a dir.
            if path.is_file():
                if self.accept(path):
                    yield path

            elif path.is_dir():
                for child in path.rglob("*"):
                    if child.is_file() and self.accept(child):
                        yield child
