import ast
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

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
    conviction_list: list[Conviction]