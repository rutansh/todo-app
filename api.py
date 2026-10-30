"""Web backend: a small JSON API and the single-page UI, on top of ``TodoStore``.

Run with: ``uv run uvicorn api:app --reload``
"""

from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from todo import TodoStore

STATIC_DIR = Path(__file__).parent / "static"
DEFAULT_FILE = Path(os.environ.get("TODO_DATA_FILE", "todos.json"))


class TaskIn(BaseModel):
    """Request body for creating a task."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)


class TaskOut(BaseModel):
    """A task as returned by the API."""

    task_id: int
    title: str
    is_done: bool


def create_app(path: Path = DEFAULT_FILE) -> FastAPI:
    """Build the app. ``path`` is the JSON file that stores the tasks."""
    app = FastAPI(title="Todo App")
    store = TodoStore(path)

    @app.get("/api/tasks")
    def list_tasks() -> list[TaskOut]:
        return [TaskOut(**asdict(task)) for task in store.list_tasks()]

    @app.post("/api/tasks", status_code=201)
    def add_task(body: TaskIn) -> TaskOut:
        return TaskOut(**asdict(store.add(body.title)))

    @app.post("/api/tasks/{task_id}/complete")
    def complete_task(task_id: int) -> TaskOut:
        try:
            return TaskOut(**asdict(store.complete(task_id)))
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=exc.args[0]) from exc

    @app.get("/", include_in_schema=False)
    def home() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    return app


app = create_app()
