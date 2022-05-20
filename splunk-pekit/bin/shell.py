#!/usr/bin/env python3
# coding: utf-8

import os
import pathlib
import subprocess
import sys
import time

root = pathlib.Path(__file__).resolve()

sys.path.insert(0, str(root.parents[1] / "lib"))

from splunklib.searchcommands import dispatch, Configuration, GeneratingCommand, Option
from splunklib.searchcommands.validators import Boolean, Duration

@Configuration()
class ShellCommand(GeneratingCommand):
    command = Option(require=True)
    shell = Option(default=True, validate=Boolean())
    timeout = Option(validate=Duration())

    def generate(self):
        record = {
            "_raw": None,
            "_time": time.time(),
            "code": None,
            "command": self.command,
            "duration": 0,
            "shell": self.shell,
            "stderr": None,
            "stdout": None,
            "timeout": self.timeout,
        }

        if self.command:
            try:
                feedback = subprocess.run(
                    self.command,
                    capture_output=True,
                    encoding="utf-8",
                    shell=self.shell,
                    text=True,
                )

            except subprocess.TimeoutExpired as exception:
                feedback = exception

            record["code"] = feedback.returncode
            record["duration"] = time.time() - record["_time"]
            record["stderr"] = feedback.stderr
            record["stdout"] = feedback.stdout

            record["_time"] = time.time()

        record["_raw"] = f"{record['command']} [{record['code']}]"

        yield record

dispatch(ShellCommand, sys.argv, sys.stdin, sys.stdout, __name__)
