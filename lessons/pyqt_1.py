import multiprocessing.dummy
import platform
from ipaddress import ip_address
from subprocess import Popen, PIPE
from tabulate import tabulate

ip_list = ["yandex.ru", "mail.ru", "google.com", "192.168.0.1"]
headers = ["Address", "Status"]


def task_1(ip_addresses):
    p = multiprocessing.dummy.Pool(5)
    ping_res = p.map(host_ping, [x for x in ip_addresses])
    res_output(ping_res, ip_addresses)


def task_2():
    star_ip = input("Please input first IP: ")
    try:
        ipv4 = check_address(star_ip)
    except Exception:
        return
    last_oct = int(star_ip.split('.')[3])
    end_ip = input("Please input how many IP should be checked: ")
    if not end_ip.isnumeric():
        print("Next time please give me a NUMBER MFKer!")
        return
    elif last_oct + int(end_ip) > 256:
        print("It's too much for me")
        return
    else:
        host_range_ping(ipv4, int(end_ip))


def check_address(_address):
    try:
        res = ip_address(_address)
    except ValueError:
        raise Exception("Wrong address: %s" % _address)
    return res


def res_output(res, adr_list):
    result = []
    for i in range(len(adr_list)):
        if res[i]:
            result.append((adr_list[i], "Reachable"))
        else:
            result.append((adr_list[i], "Unreachable"))
    print(tabulate(result, headers=headers))


def host_ping(_address):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '3', _address]
    try:
        reply = Popen(args, stdout=PIPE, stderr=PIPE)
        code = reply.wait()
    except ValueError:
        print(f"WRONG IP ADDRESS {_address}")
        return False
    if code == 0:
        return True
    return False


def host_range_ping(start, end):
    return task_1([str(start + _) for _ in range(end)])


def host_range_ping_tab():
    pass


def main():
    # task_1(ip_list)
    task_2()


if __name__ == "__main__":
    main()
