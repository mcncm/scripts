#! /bin/python

from psutil import cpu_percent

print('cpu {}%'.format(round(cpu_percent())))
