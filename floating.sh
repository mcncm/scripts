#!/usr/bin/env bash

# borrowed from Synthetica9:
# https://github.com/Synthetica9/sway-floating/blob/master/floating

$@ &
pid=$!

swaymsg -t subscribe -m '[ "window" ]' \
    | jq --unbuffered --argjson pid "$pid" '.container | select(.pid == $pid) | .id' \
    | xargs -I '@' -- swaymsg '[ con_id=@ ] floating enable' &

subscription=$!

# Wait for our process to close
tail --pid=$pid -f /dev/null

kill $subscription
