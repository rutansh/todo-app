"""Fill an empty todo list with sample tasks for demos: ``uv run python seed.py``."""

from __future__ import annotations

from pathlib import Path

from api import DEFAULT_FILE
from todo import TodoStore

SAMPLE_TASKS = [
    ("Book dentist appointment", True),
    ("Prepare slides for Friday's demo", True),
    ("Review the open pull requests", False),
    ("Renew the team's domain name", False),
    ("Plan next sprint", False),
]


def seed(path: Path = DEFAULT_FILE) -> int:
    """Add the sample tasks. Does nothing if the list already has tasks.

    Returns:
        The number of tasks added.
    """
    store = TodoStore(path)
    if store.list_tasks():
        return 0
    for title, is_done in SAMPLE_TASKS:
        task = store.add(title)
        if is_done:
            store.complete(task.task_id)
    return len(SAMPLE_TASKS)


if __name__ == "__main__":
    added = seed()
    print(f"added {added} sample tasks" if added else "list is not empty; nothing added")
