import re
from .report import Issue, Location, Coordinate


class OutputProcessingError(Exception):
    pass


class CLIOutputProcessor:
    def __init__(self, result):
        self.result = result

    def clean(self):
        pass

    def process_issues(self):
        print(f"======{self.result.stderr.decode()}======")
        print(f"======{self.result.stdout.decode()}======")
        if self.result.returncode not in self.ALLOWED_EXIT_CODES:
            raise OutputProcessingError(f"Invalid exit code {self.result.returncode}")

        return self.get_issues()


class Pep8CLIOutputProcessor(CLIOutputProcessor):
    ALLOWED_EXIT_CODES = [0, ]
    output_stream = "stdout"

    def get_issues(self):
        regex = re.compile(
            r"(?P<filename>[\w\.\/-]+):(?P<line>\d+):((?P<column>\d+):)? (?P<error_code>[\w\-]+) (?P<message>.*)"
        )

        def matcher(line: str) -> Issue:
            matches = regex.match(line)
            if not matches:
                return

            line = int(matches.group('line')) if matches.group('line') else 0
            column = int(matches.group('column')) if matches.group('column') else 0

            return Issue(
                location=Location(
                    path=matches.group('filename'),
                    begin=Coordinate(
                        line, column
                    ),
                    end=Coordinate(
                        line, column
                    ),
                ),
                issue_code=matches.group('error_code'),
                issue_text=matches.group('message'),
            )

        resultlines = getattr(self.result, self.output_stream).decode().split("\n")
        return list(filter(None, [matcher(line) for line in resultlines]))
