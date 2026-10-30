# todo-app

A basic todo app with a web UI, a JSON API and a command line (`todo.py` storage, `api.py`
backend, `static/index.html` UI, `cli.py`, tests). It is a practice codebase for the shared
agents and skills in [`agent-hub`](https://github.com/rutansh/agent-hub), which are installed
here with APM. Use it for **both** small features and big epics.

## Run the app

```bash
uv sync
uv run python seed.py                        # optional: sample tasks (never overwrites yours)
uv run uvicorn api:app --reload              # open http://localhost:8000
```

You can add tasks and tick them off. Tasks are stored in `todos.json` (git-ignored). Set
`TODO_DATA_FILE` to use another file. Interactive API docs are at `/docs`.

| Method | Path | Does |
| --- | --- | --- |
| `GET` | `/api/tasks` | List all tasks |
| `POST` | `/api/tasks` | Add a task, body `{"title": "buy milk"}` |
| `POST` | `/api/tasks/{id}/complete` | Mark a task done |

The same data is available from the command line:

```bash
uv run python cli.py add "buy milk"
uv run python cli.py list
uv run python cli.py done 1
```

## Setup (once)

```bash
brew install apm
apm install              # pulls the agents and skills pinned in apm.lock.yaml
uv sync
uv run pytest            # 17 tests pass
```

After `apm install`:

```
.cursor/agents/    architect, planner, builder
.agents/skills/    start-task, implement-feature, jira-tickets, stacked-mrs, connect-tools, ...
```

## Credentials (only if you want agents to create tickets or open MRs)

Coding and testing need no credentials. Add your own to a git-ignored `.env` file:

```bash
cp .env.example .env     # fill in only the tools you use
source .agents/skills/connect-tools/scripts/connect.sh   # loads .env and checks the tools
```

| Tool | Used for | Variables |
| --- | --- | --- |
| `acli` | Jira tickets | `JIRA_SITE`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY` |
| `glab` | Stacked MRs on GitLab | `GITLAB_TOKEN`, `GITLAB_HOST` |
| `gh` | Chained PRs on GitHub | `GH_TOKEN` |

`.env` is ignored by git and by Cursor. Never paste tokens into the chat.

## Try it

Open this folder in Cursor and start every task the same way:

> Use start-task. <what you want>

The agent asks whether it is a **small feature** or a **big epic** and runs the matching flow.

### Small feature (one MR)

- "Add due dates to tasks and show them in the UI, the API and `list`."
- "Add a way to delete a task: an API endpoint, a button in the UI and a `delete` command."
- "Add a filter that hides finished tasks, in the UI and with a `--pending` flag on `list`."

Expected: the agent reads `todo.py`, `api.py`, `static/index.html`, `cli.py` and `tests/`,
writes tests first, implements the change, runs `uv run pytest`, and asks before pushing
anything. With `--reload` the server restarts by itself, so refresh the browser to see it.

### Big epic (design, tickets, stack of MRs)

- "Add team workspaces: users can create a workspace, invite teammates, share task lists, and
  get notified when a shared task is completed."

Expected: `architect` asks design questions and writes `docs/epics/<slug>/design.md`;
`planner` splits it into tasks and creates the Jira tickets; `builder` implements each task
and ships a stack of merge requests. You approve at the end of each phase.

## Update the shared agents and skills

Change the version in `apm.yml` (for example `#v0.4.0`), then `apm install --update`.
