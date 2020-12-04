#! /usr/bin/env bash

# First, change to the indicated directory and do everything in there.
cd $1

python - <<____HERE
thing_to_print='stuff'
print(thing_to_print)
____HERE
