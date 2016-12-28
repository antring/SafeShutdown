import os
import threading
import time
import datetime
import configparser

from subprocess import check_output
from os import system


class ConfigReader:
    def __init__(self):
        self.config = configparser.ConfigParser()

        self.config['Misc'] = {'Delay in seconds': '10', 'Number of dropped packets': '5'}
        self.config['Hosts'] = {'Primary': '8.8.8.8', 'Secondary': ''}

        if not os.path.exists("config.ini"):
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
                print('(!) Config.ini not found \n(!) Config.ini generated')
                exit(1)
        else:
            self.config.read("config.ini")
            print("(*) Config loaded")


def has_ping(host):
    try:
        check_output("ping -c 1 " + host, shell=True)
    except Exception as e:
        return False
    return True


class times_missed_handler:
    def __init__(self):
        self.times_missed = 0

    def times_missed_handler(self):
        self.times_missed += 1


def task(conf, tmh):
    logfile = open("logfile.txt", "a")

    if has_ping(conf.config['Hosts']['Primary']) or has_ping(conf.config['Hosts']['Secondary']):
        missing_link = False
        tmh.times_missed = 0

        print("(*) - Link active - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logfile.write("(*) - Link active - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")

    else:
        missing_link = True
        tmh.times_missed_handler()
        print(
            "(*) - Link missing! - Missed contact: " + str(tmh.times_missed) + " - " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'))
        logfile.write(
            "(*) - Link missing! - Missed contact: " + str(tmh.times_missed) + " - " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + "\n")

    if missing_link and int(tmh.times_missed) == int(conf.config['Misc']['Number of dropped packets']):
        logfile.write("(!) Shutdown initiated - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        logfile.close()
        print(("(!) Shutdown initiated - " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        system("sudo shutdown")

    logfile.close()


def run(interval, work_function, config, tmh, it=0):
    if it != 1:
        threading.Timer(interval, run, [interval, work_function, config, tmh, 0 if it == 0 else it - 1]).start()

    work_function(config, tmh)


def main():
    conf = ConfigReader()
    tmh = times_missed_handler()
    run(int(conf.config['Misc']['Delay in seconds']), task, conf, tmh)


if __name__ == '__main__':
    main()
