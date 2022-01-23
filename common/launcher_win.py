"""Лаунчер"""

import subprocess


class WinLauncher:
    process = []

    def launch_apps(self):
        while True:
            action = input('Выберите действие: q - выход, '
                           's - запустить сервер и клиенты, x - закрыть все окна: ')

            if action == 'q':
                break
            elif action == 's':
                self.process.append(subprocess.Popen('python server.py',
                                                     creationflags=subprocess.CREATE_NEW_CONSOLE))
                for i in range(1):
                    self.process.append(subprocess.Popen('python client.py -m send',
                                                         creationflags=subprocess.CREATE_NEW_CONSOLE))
                for i in range(3):
                    self.process.append(subprocess.Popen('python client.py -m listen',
                                                         creationflags=subprocess.CREATE_NEW_CONSOLE))
            elif action == 'x':
                while self.process:
                    victim = self.process.pop()
                    victim.kill()
