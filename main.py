from api.config import config
from api.reporter import Pep8CLIOutputProcessor
from api.runner import CLIRunner


class AnsibleCLIRunner(CLIRunner):
    report_processor = Pep8CLIOutputProcessor

    @property
    def command(self):
        return ["ansible-lint", "-p", *config.files]


def main():
    AnsibleCLIRunner().run()


if __name__ == '__main__':
    main()
