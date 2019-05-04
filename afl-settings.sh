# mcncm 2019

# This is the file to be modified
CORE_PATTERN_FILE="/proc/sys/kernel/core_pattern"
# One of these strings should be the only line in core_pattern! 
OFF_STRING="|/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %h %e"
ON_STRING="core"

function afl_start {
	echo "Modifying core_pattern..."
	echo $ON_STRING > $CORE_PATTERN_FILE
	echo "Modifying CPU frequency scaling..."
	(cd /sys/devices/system/cpu &&\
	echo performance | tee cpu*/cpufreq/scaling_governor)
}

function afl_stop {
	echo "Reverting core_pattern..."
	echo $OFF_STRING > $CORE_PATTERN_FILE
	echo "Reverting CPU frequency scaling..."
	(cd /sys/devices/system/cpu &&\
	echo powersave | tee cpu*/cpufreq/scaling_governor)
}

function afl_other {
	echo "I'm not sure what to do with that instruction."
	echo "Try `$ afl start` or `afl stop`"
}

case $1 in
	on)		afl_start	;;
	off)	afl_stop	;;
	*)		afl_other	;;
esac
