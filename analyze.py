import os

from helper import (
    make_issue,
    prepare_result,
    publish_results,
    get_files,
)

codepath = os.environ.get("CODE_PATH", "/code")

resultpath = "/tmp/results.json"
app_path = os.path.dirname(os.path.abspath(__file__))

analysis_command = [
    "/toolbox/venv/bin/ansible-lint",
    "-p",
    get_files(codepath).join(" "),
]

def _get_issues():
    """Run the checks."""
    issues = []
    if not files_to_analyze:
        return issues

    # There are files to analyze
    result = subprocess.run(
        analysis_command,
        capture_output=True,
    )

    # Read the json, convert it into DS's format.
    with open(resultpath) as fp:
        raised_issues = json.load(fp)["results"]
    for issue in raised_issues:
        issue_code = issue["check_id"].split("::")[-1]
        issue_text = issue["extra"]["message"]
        filepath = issue["path"]
        startline = issue["start"]["line"]
        startcol = issue["start"]["col"]
        endline = issue["end"]["line"]
        endcol = issue["end"]["col"]
        issues.append(
            make_issue(
                issue_code, issue_text, filepath, startline, startcol, endline, endcol
            )
        )

    return issues

issues = _get_issues()

# Publish to DeepSource
publish_results(prepare_result(issues))


class Report:
    def __init__(self):
        self.issues = []
        self.errors = []
        self.metrics = []


class CLIOutputParser:
    def __init__(self, result):
        self.result = result

    def clean(self):
        pass

    def process_results(self):
        if self.result.returncode not in self.ALLOWED_EXIT_CODES:
            raise OutputProcessingError(f"Invalid exit code {self.result.returncode}")

        resultlines = getattr(self.result, self.output_stream).decode().split("\n")

        report = Report()

        for line in resultlines:
            report.issues.append(self._process_line(line, self.pattern_matching_func))

    def _process_line(self, line, pattern_matching_func):
        return Issue(*pattern_matching_func(line))


class Pep8CLIOutputParser(CLIOutputParser):
    ALLOWED_EXIT_CODES = [0,]
    output_stream = "stdout"

    def pattern_matching_func(self):
        regex = re.compile(
            r"(?P<filename>[\w\.\/]+):(?P<line>\d+):((?P<column>\d+:)?) (?P<error_code>[\w\-]+) (?P<message>.*)"
        )
        def matcher(line):
            matches = regex.match(line)
            return (
                matches.group('filename'),
                matches.group('line'),
                matches.group('column'),
                matches.group('error_code'),
                matches.group('message'),
            )

        return matcher


class CLIRunner(Runner):
    @property
    def command(self):
        raise NotImplementedError

    @property
    def report_processor(self):
        raise NotImplementedError

    def run(self):
        results = subprocess.run(
            self.command,
            capture_output=True,
        )

        return self.report_processor(results).process_results()


class AnsibleCLIRunner(CLIRunner):
    report_processor = Pep8CLIReportParser

    @property
    def command(self):
        return ["ansible-lint", "-p", self.files]
