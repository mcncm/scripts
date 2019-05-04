# mcncm 2019

BGDIR=$HOME/imag/wallpaper
BLDIR=$BGDIR/.blacklist
FEHFILE=$HOME/.fehbg

function checkwm {
  # Returns the window manager that's currently running; this is useful for
  # adding an auto-reload if I switch to a different one.

  if [[ ! -z $(pgrep ^sway$) ]] ; then
    echo sway
  else
    echo ""  # Empty value. Should probably return error code instead.
  fi
}

function reloadwm {
  # Reloads the window manager
  wm=checkwm
  if [[ $wm == sway ]] ; then
    swaymsg reload
  fi
}

function checkdir {
	# Check if a background is in a particular directory. The first argument
	# should be a directory, and the second a file.

	if [[ -f $1/$2 ]] ; then
		echo $2
	elif [[ -f $1/$2.jpg ]] ; then
		echo $1/$2.jpg
	elif [[ -f $1/$2.png ]] ; then
		echo $1/$2.png
	else
		echo "" # Empty value. Should probably return error code instead.
	fi
}

function checkname {
	# Check the name and echo back a valid background full path that it
	# (probably) matches.

    # TODO: fix this. Instead of repeated checking of hardcoded conditions,
    # should loop through a list of alternates.
	BGPATH=$(checkdir $BGDIR $1)
	if [[ -z $BGPATH ]] ; then
    	BGPATH=$(checkdir $BLDIR $1)
	fi
	if [[ -z $BGPATH ]] ; then
    	BGPATH=$(checkdir $BGDIR/3840x2160 $1)
	fi

    echo $BGPATH
}

function listbg {
	# List all the (non-blacklisted) files that can be selected

	echo "$(find $BGDIR -path $BLDIR -prune -o -type f)"
}

function randbg {
	# Pick a random valid background
	# Also, this is a dumb algorithm. Should just diff the files with the bg
	# list.
	BGFILES="$(listbg)"
	echo "$(listbg)" | shuf -n 1
}

function setbg {
	# Set the background to argument 1, liberally

	if [[ ! -z $1 ]] ; then
		echo '#!/bin/sh' > $FEHFILE
		echo feh --bg-fill \'$1\' >> $FEHFILE
		$HOME/.config/i3/makelockbg.sh > /dev/null &
	fi
    # Call wal to set the new theme colors.
    wal -e -i $1 -a 80 -q
    # Now reload the window manager, setting the background in the process.
    reloadwm
}

function blacklist {
	# Add a wallpaper to the blacklist file: it will not be selected by rand.
	
	mv $1 $BLDIR
}

function whitelist {
	# Remove a wallpaper from the blacklist file
	# Note that this won't always have the right behavior. 
	
	mv $1 $BGDIR	
}

function info {
	# Print info on backgrounds

	echo "Here are some wallpapers you can choose from!"
	echo "$(listbg)"
	#find $BGDIR -path $BLDIR -prune -o -type f | basename
}

function main {
	case $1 in
		"")     info                      ;;
		rand)   setbg $(randbg)           ;;
		bl)     blacklist $(checkname $2) ;;
		wl)     whitelist $(checkname $2) ;;
		*)      setbg $(checkname $1)     ;;
	esac
}

main $1 $2
