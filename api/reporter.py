import re
from .report import Report, Issue, Location, Coordinate


class OutputProcessingError(Exception):
    pass


class CLIOutputProcessor:
    def __init__(self, result):
        self.result = result

    def clean(self):
        pass

    def process_results(self):
        if self.result.returncode not in self.ALLOWED_EXIT_CODES:
            raise OutputProcessingError(f"Invalid exit code {self.result.returncode}")

        report = Report()
        # TODO: Add for metrics and errors
        report.issues = self.get_issues()
        report.write()

        return report


class Pep8CLIOutputProcessor(CLIOutputProcessor):
    ALLOWED_EXIT_CODES = [0, ]
    output_stream = "stdout"

    def get_issues(self):
        regex = re.compile(
            r"(?P<filename>[\w\.\/]+):(?P<line>\d+):((?P<column>\d+:)?) (?P<error_code>[\w\-]+) (?P<message>.*)"
        )

        def matcher(line: str) -> Issue:
            matches = regex.match(line)
            if not matches:
                return

            return Issue(
                location=Location(
                    path=matches.group('filename'),
                    begin=Coordinate(
                        matches.group('line'), matches.group('column'),
                    ),
                    end=Coordinate(
                        matches.group('line'), matches.group('column'),
                    ),
                ),
                issue_code=matches.group('error_code'),
                issue_text=matches.group('message'),
            )

        resultlines = getattr(self.result, self.output_stream).decode().split("\n")
        return [matcher(line) for line in resultlines if matcher(line)]
