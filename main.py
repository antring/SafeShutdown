from subprocess import check_output
from os import system

import time

import datetime


def has_ping(host):
    try:
        check_output("ping -c 1 " + host, shell=True)
    except Exception as e:
        return False

    return True


def main():
    times_missed = 0

    while 1:
        logfile = open("logfile.txt", "a")
        missing_link = False

        if has_ping("8.8.8.8") or has_ping("www.vg.no"):
            missing_link = False
            times_missed = 0
            print("(*) - Link active - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            logfile.write("(*) - Link active - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
            logfile.close()

        else:
            missing_link = True
            times_missed += 1
            print(
                "(*) - Link missing! - Missed contact: " + str(times_missed) + " - " + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'))
            logfile.write(
                "(*) - Link missing! - Missed contact: " + str(times_missed) + " - " + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + "\n")
            logfile.close()

        if missing_link and times_missed == 3:
            logfile.write("(!) Shutdown initiated - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
            logfile.close()
            print(("(!) Shutdown initiated - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            system("sudo shutdown")

        time.sleep(300)


if __name__ == '__main__':
    main()
