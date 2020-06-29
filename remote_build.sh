#! /usr/bin/env bash

#############################################################################
# Author: mcncm, 2020
#
# A shell script for compiling C++ projects on my build server and deploying
# them to the phone over USB. This makes the cross-compilation process easier
# and lower-friction.
#
# This script makes a few assumptions about how the project is set up:
# * The project's Makefile should build for the Pinephone with `make release`
# * The build process should yield one or more binaries under ./build/bin
# * It must be directly under the root of the Pinephone project tree.
#   The build server must also have the same Pinephone project tree
#   structure.
#
# TODO
# * Is it possible to accomplish all of this *in* my Makefiles?
# * Is using this SSH master connection thing really safe in a shell script?
#   If the script is interrupted, the connection will remain open.
# * mux_master_process_new_session: tcgetattr: Inappropriate ioctl for device
# * exit gracefully on "any" kind of error and close the master connection?
# * specialized checking behavior for nixos should be handled more elegantly
# * two-step rsync copying of binary is a little awkward if the build server
#   is also the deploy target!
#
#############################################################################

# Parse options
# -b: build server (argument, name)
# -t: target (argument, name)
# -d: deploy (option)
while getopts ":b:t:d" opt; do
  case ${opt} in
    b )
      export BUILD_SERVER=$OPTARG
      ;;
    t )
      export TARGET=$OPTARG
      ;;
    d )
      DEPLOY=1
      ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      ;;
  esac
done
shift $((OPTIND -1))

# Set default values if not overridden by options
if [ -z "$BUILD_SERVER" ] ; then
  export $(grep BUILD_SERVER $HOME/.scripts/secrets.txt)
  echo "Setting BUILD_SERVER to default: $BUILD_SERVER"
fi
if [ -z "$TARGET" ] ; then
  export TARGET=pinephone-usb
  echo "Setting TARGET to default: $TARGET"
fi

LOCAL_PINE_DIR=~/proj/pinephone
LOCAL_PROJ_DIR=$(pwd)
LOCAL_BUILD_DIR=$LOCAL_PROJ_DIR/build/bin
PROJ_NAME=$(basename $LOCAL_PROJ_DIR)

REMOTE_PINE_DIR=~/proj/pinephone
REMOTE_PROJ_DIR=$REMOTE_PINE_DIR/$PROJ_NAME
REMOTE_BUILD_DIR=$REMOTE_PROJ_DIR/build/bin

PINEPHONE_BIN_DIR=~/bin

# Check that you are directly under the root of the Pinephone directory
if [[ $(dirname $LOCAL_PROJ_DIR) != $LOCAL_PINE_DIR ]] ; then
  echo "This project isn't under the root Pinephone project directory."
  exit 1
fi

# Establish a master connection
ssh -M -f -N $BUILD_SERVER

# On success, clean the local project directory
(cd $LOCAL_PROJ_DIR && make clean)

# Clear existing remote project directory
ssh -T $BUILD_SERVER << EOSSH
rm -rf $REMOTE_PROJ_DIR
mkdir -p $REMOTE_PROJ_DIR
EOSSH

# Upload the new copy
rsync -va -zz --rsh=ssh --exclude='.git' --exclude='*.bmp' $LOCAL_PROJ_DIR $BUILD_SERVER:$REMOTE_PINE_DIR

# What make command to use? Depends on whether source == target or not.
if [ $BUILD_SERVER == $TARGET ] ; then
  MAKE_TARGET=native
else
  MAKE_TARKET=cross
fi

# Build it! Must force pseudoterminal allocation for nix-shell to work (I
# think?).
ssh -tt $BUILD_SERVER << EOSSH

cd $REMOTE_PINE_DIR

RNAME=\$(cat /etc/*-release | grep "^NAME")
if [[ \${RNAME^^} == *NIXOS* ]] ; then
  IS_NIXOS=1
fi

if [ $IS_NIXOS ] ; then
  nix-shell shell.nix
fi

cd $REMOTE_PROJ_DIR
make $MAKE_TARGET

if [ $IS_NIXOS ] ; then
  exit        # exit nix-shell
fi

if [ ! -z \$(which logout) ] ; then
  logout      # logout of build server
else
  exit
fi

EOSSH

# Copy the binary back to local
scp -r $BUILD_SERVER:$REMOTE_BUILD_DIR/* $LOCAL_BUILD_DIR

# Close master connection
ssh -O exit $BUILD_SERVER

# Finally, put it on the device if you want to.
if [ $DEPLOY ] ; then
  rsync -va -zz -rsh=ssh $LOCAL_BUILD_DIR/ $TARGET:$PINEPHONE_BIN_DIR
fi
