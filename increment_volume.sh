#! /bin/bash
MONITOR_SPEAKER=\'IEC958\',0

echo $MONITOR_SPEAKER
amixer set Master $1
amixer set $MONITOR_SPEAKER $1
