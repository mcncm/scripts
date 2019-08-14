#! /bin/python

from psutil import disk_usage

print("ssd {}%".format(round(disk_usage('/')[3])))
