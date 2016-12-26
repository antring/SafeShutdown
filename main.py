from subprocess import check_output
from os import system

import time


def has_ping(host):
    try:
        check_output("ping -c 1 " + host, shell=True)
    except Exception as e:
        return False

    return True


def main():
    times_missed = 0

    while 1:
        missing_link = True

        if has_ping("8.8.8.8") or has_ping("www.vg.no"):
            missing_link = False
            times_missed = 0
            print("has_link")

        else:
            missing_link = True
            times_missed += 1
            print("missing_link")

        if missing_link and times_missed == 3:
            system("sudo shutdown")

        time.sleep(300)


if __name__ == '__main__':
    main()
