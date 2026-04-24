# Clawthon OpenClaw Project

OpenClaw-side project workspace for the Wecreate Clawthon event.

This repository contains the participant agent workflow, Wecreate API request builders, Feishu delivery helpers, tests, and operational docs needed for team collaboration.

## Current Production Context

- Wecreate event: <https://wecreate.net.cn/events/2>
- Hackathon ID: `2`
- Team ID: `10`
- Team name: `OpenClaw 冲冲冲！`
- GitHub repo: <https://github.com/lu-hongming/clawthon-openclaw-project>

Do not commit JWTs, SMS codes, Feishu webhooks, GitHub tokens, or local `.env.local` files.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp config/openclaw.env.example config/openclaw.env.local
pytest
```

Set `WECREATE_BASE_URL` and `WECREATE_ACCESS_TOKEN` in `config/openclaw.env.local` for live Wecreate API calls.

## Useful Commands

```bash
python -m clawthon_openclaw --help
python -m clawthon_openclaw list-hackathons
python -m clawthon_openclaw hackathon-detail --hackathon-id 2
python -m clawthon_openclaw my-enrollment --hackathon-id 2
```

Submission writes are team-leader gated on Wecreate. The current member account can inspect state, but final draft creation/update must be performed by the team leader account or after leadership transfer.

## Collaboration

- `main`: stable shared state.
- `agent/member-openclaw-workflow`: OpenClaw API workflow and tests.
- `agent/leader-submission`: leader-owned submission copy and final Wecreate release metadata.

See `docs/openclaw-github-collaboration.md` and `docs/openclaw-production-run-log.md` for current blockers and run history.

