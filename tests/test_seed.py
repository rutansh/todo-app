from pathlib import Path

from seed import SAMPLE_TASKS, seed
from todo import TodoStore


def test_seed_fills_an_empty_list(tmp_path: Path) -> None:
    path = tmp_path / "todos.json"
    assert seed(path) == len(SAMPLE_TASKS)
    tasks = TodoStore(path).list_tasks()
    assert [t.title for t in tasks] == [title for title, _ in SAMPLE_TASKS]
    assert [t.is_done for t in tasks] == [done for _, done in SAMPLE_TASKS]


def test_seed_never_overwrites_existing_tasks(tmp_path: Path) -> None:
    path = tmp_path / "todos.json"
    TodoStore(path).add("My real task")
    assert seed(path) == 0
    assert [t.title for t in TodoStore(path).list_tasks()] == ["My real task"]
