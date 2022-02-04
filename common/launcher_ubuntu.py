"""
It is a launcher for starting subprocesses for server and clients of two types: senders and listeners.
for more information:
https://stackoverflow.com/questions/67348716/kill-process-do-not-kill-the-subprocess-and-do-not-close-a-terminal-window
"""

import os
import signal
import subprocess
import sys
from time import sleep

PYTHON_PATH = sys.executable
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class UbuntuLauncher:
    process = []

    def get_subprocess(self, file_with_args):
        sleep(0.2)
        file_full_path = f"{PYTHON_PATH} {BASE_PATH}/{file_with_args}"
        args = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", file_full_path]
        return subprocess.Popen(args, preexec_fn=os.setpgrp)

    def launch_apps(self):
        while True:
            text_for_input = "Выберите действие: q - выход, s - запустить сервер и клиенты, x - закрыть все окна: "
            action = input(text_for_input)

            if action == "q":
                break
            elif action == "s":
                self.process.append(self.get_subprocess("server.py"))

                for i in range(2):
                    self.process.append(self.get_subprocess("client.py -m send"))

                for i in range(2):
                    self.process.append(self.get_subprocess("client.py -m listen"))

            elif action == "x":
                while self.process:
                    victim = self.process.pop()
                    os.killpg(victim.pid, signal.SIGINT)
