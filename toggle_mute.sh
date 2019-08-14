# Make my mute button work the way I expect it to. This is an ugly hack,
# but it works.

# mcncm 2019

MONITOR_SPEAKER=\'IEC958\',0

if [[ -z $(amixer get Master | grep off) ]] ; then
  amixer set Master off
  amixer set $MONITOR_SPEAKER off
  echo off!
else
  amixer set Master on
  amixer set $MONITOR_SPEAKER on
  amixer set Speaker on
  amixer set Headphone on
fi
