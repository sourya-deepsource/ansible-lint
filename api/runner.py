import subprocess


class CLIRunner:
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
