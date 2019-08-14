#! /bin/python

from psutil import sensors_battery

print('bat {}%'.format(round(sensors_battery()[0])))

