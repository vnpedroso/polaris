import ast
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

from colorama import Fore, Back, Style

class Severity(IntEnum):
    WARNING = 0
    ERROR   = 1

@dataclass(frozen=True)
class Offense:
    node:       ast.AST
    message:    str
    severity:   Severity

@dataclass(frozen=True)
class Conviction:
    offense:        Offense
    offense_code:   str
    file_name:      str

@dataclass(frozen=False)
class Sentence:
    convictions: list[Conviction]


class BaseChecker(ast.NodeVisitor):
    def __init__(self, offense_code):
        self.offense_code   = offense_code
        self.offenses       = set()

class Linter:

    SENTENCE_FMT = "{:.<55} {}: {}"

    def __init__(self):
        self.checkers   = set()
        self.sentence   = Sentence([])
        self.exit_code  = Severity.WARNING # default exit code is 0

    def _offense_code_fmt(self, conviction: Conviction) -> str:
        offense_code = conviction.offense_code
        return f"{Back.BLUE}{offense_code}{Style.RESET_ALL}"

    def _severity_fmt(self, conviction: Conviction) -> str:
        color       = Fore.YELLOW
        severity    = conviction.offense.severity

        if severity == Severity.ERROR:
            color = Fore.RED

        return f"{color}{severity.name}{Style.RESET_ALL}"


    def run(self, file: Path):

        with open(file, "r", encoding="utf-8") as f:
            code = f.read()

        file_name   = file.name
        tree        = ast.parse(code)

        for checker in self.checkers:
            checker.offenses = set()
            checker.visit(tree)

            for offense in checker.offenses:
                conviction = Conviction(
                                offense_code    = checker.offense_code,
                                file_name       = file_name,
                                offense         = offense,
                            )

                self.sentence.convictions.append(conviction)

                # bitwise OR for the exit code, a single 1 is all it takes...
                self.exit_code |= offense.severity

        return


    def print_sentence(self):
        sentence = self.sentence

        if sentence:
            for conviction in sentence.convictions:
                scope_start         = conviction.offense.node.lineno
                scope_end           = conviction.offense.node.end_lineno
                file_name           = conviction.file_name
                message             = conviction.offense.message
                offense_code        = self._offense_code_fmt(conviction)
                severity            = self._severity_fmt(conviction)

                output = self.SENTENCE_FMT.format(
                    f"{file_name}:{scope_start}:{scope_end}",
                    f"{offense_code}:{severity}",
                    message
                )

        print(output)