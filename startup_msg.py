#! /usr/bin/env python

import os
import pprint
import random
import re
import textwrap
from typing import List, Optional, Callable

from termcolor import cprint

TODO_FILES = [
    os.path.join(os.environ['ORG_DIR'], 'agenda', 'personal.org')
]

TODO_HEADLINE_PATTERN = re.compile(r'\s*\**\s*TODO')


def print_item(title: str, content: str) -> str:
    cprint(title, attrs=['bold'])
    content_fmted = textwrap.indent(content, 8 * ' ')
    cprint(content_fmted, 'blue')


########################################
# Listing TODOs from tracked org files #
########################################


def _guess_agenda_files() -> List[str]:
    """Attempts to figure out agenda files from emacs config
    """
    try:
        emacs_config = os.path.join(os.path.expanduser('~'), '.spacemacs')
        with open(emacs_config, 'r') as f:
            agenda_line = next(line for line in f.readlines()
                               if 'org-agenda-files' in line)
        agenda_files = re.findall(r'"(.*?)"', agenda_line)
        return map(os.path.expanduser, agenda_files)

    except StopIteration:
        return TODO_FILES


def _is_todo_headline(line: str) -> bool:
    """True if this is a todo headline
    """
    return bool(re.match(TODO_HEADLINE_PATTERN, line))


def _get_todo(line: str) -> str:
    """Assuming that this line is a todo headline, return the todo
    """
    return line.split('TODO', maxsplit=1)[1].lstrip()


def _file_todos(fn: str) -> List[str]:
    """Get all the newline-terminated todo headlines from a single todo file
    """
    with open(fn, 'r') as f:
        lines = f.readlines()
    return (_get_todo(line) for line in lines if _is_todo_headline(line))


def _all_todos() -> List[str]:
    """Get all the newline-terminated todo headlines from every file in the
    searched files.
    """
    agenda_files = _guess_agenda_files()
    return [todo for fn in agenda_files for todo in _file_todos(fn)]


def get_random_todos(samples: int) -> List[str]:
    """Select random todos from the searched files. This function is "public" for
    this section.
    """
    assert samples > 0
    all_todos = _all_todos()
    samples = min(samples, len(all_todos))
    return random.sample(all_todos, k=samples)


if __name__ == '__main__':
    to_print = {
        'Todos:': ''.join(get_random_todos(3)),
    }

    for title, content in to_print.items():
        try:
            print_item(title, content)
        except Exception:
            print("Failed to produce item '{}'.\n".format(title))
