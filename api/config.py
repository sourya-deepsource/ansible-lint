import json
import os

from functools import cached_property


class AnalysisConfig:
    @cached_property
    def analysis_config(self):
        with open(f"{os.getenv('TOOLBOX_PATH')}/analysis_config.json") as f:
            contents = f.read()

        return json.loads(contents)

    @property
    def files(self):
        return self.analysis_config["files"]


config = AnalysisConfig()
