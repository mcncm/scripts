#! /bin/python

from psutil import virtual_memory
print("ram {}%".format(round(virtual_memory()[2])))
