# demo-small-feature

**Demo:** ask an AI agent for a small feature and watch it use the team's shared skills.

The code is a tiny todo app (`todo.py`, `cli.py`, tests). The shared agents and skills come
from [`agent-hub`](https://github.com/rutansh/agent-hub) through APM.

## Setup (once)

```bash
brew install apm
gh auth login            # agent-hub is private
apm install              # pulls the agents and skills pinned in apm.lock.yaml
uv sync                  # python deps
uv run pytest            # 6 tests pass
```

After `apm install` you will see:

```
.cursor/agents/    architect, planner, builder
.agents/skills/    start-task, implement-feature, jira-tickets, stacked-mrs, ...
```

## Credentials (only if you want it to open a merge request)

Coding and testing need no credentials. To let the agent open an MR or PR, add your own to
a git-ignored `.env` file:

```bash
cp .env.example .env     # fill in GH_TOKEN (GitHub) or GITLAB_TOKEN + GITLAB_HOST (GitLab)
source .agents/skills/connect-tools/scripts/connect.sh   # loads .env and checks the tools
```

`.env` is ignored by git and by Cursor. Never paste tokens into the chat.

## The demo

Open this folder in Cursor and type:

> Use start-task. I want to add due dates to tasks.

What should happen:

1. The agent asks: **small feature or big epic?** Answer: **small feature**.
2. It reads `todo.py`, `cli.py` and `tests/` to learn the conventions.
3. It adds tests first, then implements `--due YYYY-MM-DD` on `add` and shows the due
   date in `list`.
4. It runs `uv run pytest` and reports the result.
5. It asks before pushing anything.

Other small features to try:

- "Add a `delete` command."
- "Add a `--pending` flag to `list` that hides finished tasks."

## What this shows

One `apm install` gives every developer the same workflow. Nobody copies prompts around.

## Update the shared skills

Change the version in `apm.yml` (for example `#v0.3.0`), then:

```bash
apm install --update
```

See also: [`demo-big-epic`](https://github.com/rutansh/demo-big-epic) for the
multi-agent epic workflow.
