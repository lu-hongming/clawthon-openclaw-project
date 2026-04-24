# OpenClaw Foundation

This directory contains the first OpenClaw-side building blocks for Clawthon.

## Current modules

- `clawthon_openclaw/persona.py`
  - loads and normalizes local agent persona configs
- `clawthon_openclaw/audit.py`
  - defines the structured audit event payload
- `clawthon_openclaw/audit_writer.py`
  - persists audit events as JSONL traces
- `clawthon_openclaw/client.py`
  - provides the base Wecreate API configuration and request builders
- `clawthon_openclaw/settings.py`
  - loads Wecreate runtime access from environment variables
- `clawthon_openclaw/profile_mapper.py`
  - maps local persona data to Wecreate profile fields
- `clawthon_openclaw/transport.py`
  - prepares JSON HTTP requests and provides a minimal urllib transport
- `clawthon_openclaw/sync.py`
  - syncs local persona to the Wecreate `/api/v1/users/me` endpoint
- `clawthon_openclaw/workflows.py`
  - wraps enrollment and AI team-match requests with audit logging
- `clawthon_openclaw/remaining_workflows.py`
  - wraps hackathon detail, enrollment state, team create, team join, and Feishu notification
- `clawthon_openclaw/delivery.py`
  - standardizes GitHub branch/tag/message helpers and submission metadata
- `clawthon_openclaw/feishu.py`
  - formats Feishu text notifications and webhook requests
- `clawthon_openclaw/timeline.py`
  - renders JSONL audit traces into markdown timelines
- `clawthon_openclaw/cli.py`
  - exposes a minimal command parser for demo-oriented commands

## Local conventions

- Persona files live under `config/personas/`
- The first sample persona is `config/personas/example-agent.json`
- Audit events should always carry:
  - `trace_id`
  - `agent_id`
  - `phase`
  - `skill_name`
  - `action_name`
  - `status`

## Next steps

1. Bind CLI commands to the real workflows and environment loading.
2. Add submission create or update workflow using the delivery helpers.
3. Add GitHub and Feishu live execution using real credentials.
4. Add a single demo script that chains the full autonomous flow.
