import json
import os

from dataclasses import dataclass


CODEPATH = os.environ.get("CODE_PATH")


@dataclass
class Coordinate:
    line: int
    column: int

    def as_dict(self):
        return {
            "line": self.line,
            "column": self.column,
        }


@dataclass
class Location:
    path: str
    begin: Coordinate
    end: Coordinate

    def as_dict(self):
        return {
            "path": self.path[len(CODEPATH):] if self.path.startswith(CODEPATH) else self.path,
            "position": {
                "begin": self.begin.as_dict(),
                "end": self.end.as_dict(),
            }
        }


@dataclass
class Issue:
    location: Location
    issue_code: str
    issue_text: str

    def as_dict(self):
        return {
            "location": self.location.as_dict(),
            "issue_text": self.issue_text,
            "issue_code": self.issue_code,
        }


class Report:
    def __init__(self):
        self.issues = []
        self.errors = []
        self.metrics = []

    def write(self, path=None):
        if not path:
            path = f"{os.environ.get('TOOLBOX_PATH')}/analysis_results.json"

        with open(path, "w") as f:
            f.write(
                json.dumps(
                    {
                        "errors": [error.as_dict() for error in self.errors],
                        "issues": [issue.as_dict() for issue in self.issues],
                        "metrics": [metric.as_dict() for metric in self.metrics],
                    },
                ),
            )
