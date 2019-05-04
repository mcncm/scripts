#! /bin/python

import sys

if len(sys.argv) < 2:
    powers = 25
else:
    try:
        powers = int(sys.argv[1])
    except ValueError:
        print("I'm not sure how to interpret that number.")
        sys.exit()

for i in range(1, powers + 1):
  print(str(i).ljust(3) + str(2**i))
