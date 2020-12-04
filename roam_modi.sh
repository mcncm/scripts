#! /usr/bin/env bash

if [ -z $@ ]
then
    ls ~/org/roam/*.org
else
    FILE=$@

    # TODO handle the case where it's a new entry
    swaymsg 'set $PROP floating ; exec emacsclient --create-frame' "$FILE" > /dev/null
fi
