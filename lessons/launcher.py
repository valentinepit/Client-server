from sys import platform
from common.launcher_win import WinLauncher
from common.launcher_ubuntu import UbuntuLauncher
from common.launcher_mac import MacLauncher


def choose_os():

    if platform == "linux" or platform == "linux2":
        _launcher = UbuntuLauncher()
    elif platform == "darwin":
        _launcher = MacLauncher()
    elif platform == "win32":
        _launcher = WinLauncher()
    else:
        raise ValueError
    return _launcher


def main():
    launcher = choose_os()
    launcher.launch_apps()


if __name__ == '__main__':
    main()
