# mcncm 2019

ORGDIR=$HOME/text/org
DEFAULT=todo.org

function open_org {
  nohup emacs $1 &> /dev/null & 
}

function open_default {
  open_org $ORGDIR/$DEFAULT
}

function commit-dir {
  # Stage and commit the whole org repository with a commit message
  (cd $ORGDIR && git add -A && git commit -m "$1")
}

function org_diff {
  (cd $ORGDIR && git diff)
}

function default_commit {
  # Commit with a default message: just a timestamp.
  commit_dir "$(date +%Y-%m-%d\ %H:%M:%S)"
}

function clean_old_commits {
  # Absolutely wipe out the history
  echo ""
}

function main {
  if [ $# -eq 0 ] ; then
    open_default
  fi
  case $1 in
    commit)         default_commit      ;;
    diff)           org_diff            ;;
    clean)          clean_old_commits   ;;
  esac
}

main "$@"
