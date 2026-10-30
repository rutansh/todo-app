# demo-trial-analyst

Demo project showing how a team consumes shared skills from
[`ai4pharma-skills`](https://github.com/rutansh/ai4pharma-skills) with APM.

This project installs **all** skills from the central repo, pinned to `v0.1.0`.

## Setup

```bash
brew install apm        # once per machine
gh auth login           # the skills repo is private; APM uses your GitHub auth
apm install             # reads apm.yml + apm.lock.yaml, deploys skills
```

Skills land in `.agents/skills/`, where Cursor picks them up.

## Try it

Open this folder in Cursor and ask the agent:

> Summarize `data/sample-trial.md`

The agent should apply the `clinical-trial-summary` skill and produce the structured
brief, listing anything the source does not state.

You can also try:

> Write a literature review brief from the abstracts in `data/sample-trial.md`

## Update to a newer skills release

```bash
# edit the ref in apm.yml (e.g. #v0.2.0), then:
apm install --update
```

## Notes

- All data in `data/` is **fictional** and for demo purposes only.
- `apm_modules/` is git-ignored. `apm.lock.yaml` is committed so everyone gets
  identical skills.
