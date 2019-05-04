# Config/theme switcher. 
# mcncm 2019


DOTFILES_DIRECTORY=$HOME/.dotfiles


function abs_path {
  # Get the absolute path of a file from a theme name and relative path
  local REL_PATH=$1
  echo $DOTFILES_DIRECTORY/$THEME/$REL_PATH
}

function link_file () {
  # Given theme name and path to a file, link it into the home tree.
  local REL_PATH=$1
  local TARGET_PATH=$HOME/$REL_PATH
  
  # Check what's currently living at that location
  if [[ -f $TARGET_PATH && ! -L $TARGET_PATH ]] ; then
    # If there's a file there, break here
    return
  elif [[ -L $TARGET_PATH ]] ; then
    unlink $TARGET_PATH
  fi

  # Finally, if we haven't broken out, relink. cwd should be directory of file.
  ln -s $(abs_path $REL_PATH) $TARGET_PATH
}

function link_dir () {
  # Recursively link the contents of a theme directory, carefully.

  # Relative path of this directory to the theme directory
  local REL_PATH=$1
  
  local ABS_PATH=$(abs_path $REL_PATH)

  for f in $(ls -a $ABS_PATH); do
    # For now, disallow symlinks within a theme tree.
    if [[ $f == . || $f == .. || -L $ABS_PATH/$f ]] ; then
      continue
    elif [[ -d $ABS_PATH/$f ]] ; then
      link_dir $REL_PATH/$f
    else
      link_file $REL_PATH/$f
    fi
  done
}

function switch_theme () {
  # Switches to the theme named in the first argument
  THEME=$1
  link_dir ""
}

# Switch to the first argument's theme
switch_theme $1
