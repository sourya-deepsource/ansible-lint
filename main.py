from api.config import config
from api.reporter import Pep8CLIOutputProcessor
from api.runner import CLIRunner


ISSUE_CODES_MAP = {
    "git-latest": "E4001",
    "hg-latest": "E4002",
    "package-latest": "E4003",
    "no-relative-paths": "E4004",

    "partial-become": "E5001",
    "unnamed-task": "E5002",
    "no-handler": "E5003",
    "deprecated-local-action": "E5004",

    "no-changed-when": "E3001",
    "deprecated-command-syntax": "E3002",
    "command-instead-of-module": "E3003",
    "inline-env-var": "E3004",
    "command-instead-of-shell": "E3005",
    "risky-shell-pipe": "E3006",
}


class AnsibleLintOutputParser(Pep8CLIOutputProcessor):
    ALLOWED_EXIT_CODES = [0, 2]
    def get_issues(self):
        issues = super().get_issues()

        for issue in issues:
            # The issue code raised by ansible-lint are different from what DeepSource would raise
            try:
                issue_code = ISSUE_CODES_MAP[issue.issue_code]
            except KeyError:
                continue

            issue.issue_code = f"ANS-{issue_code}"

        return issues


class AnsibleCLIRunner(CLIRunner):
    report_processor = AnsibleLintOutputParser
    command = ["ansible-lint", "--nocolor", "-p", *config.files]


def main():
    AnsibleCLIRunner().run()


if __name__ == '__main__':
    main()