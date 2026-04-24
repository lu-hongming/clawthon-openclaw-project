# OpenClaw Remaining Work Table

| Priority | Workstream | Deliverable | Status |
|---|---|---|---|
| 1 | Runtime Access | `WECREATE_BASE_URL`, token, Feishu webhook env template | Done locally |
| 1 | Discovery Flow | Hackathon detail read workflow | Done |
| 1 | Enrollment Flow | Current enrollment read + create enrollment workflow | Done |
| 1 | Teaming Flow | Team create + team join workflow | Done |
| 1 | Audit | JSONL event writer + markdown timeline renderer | Done |
| 2 | Profile Sync | Persona -> `/api/v1/users/me` sync | Done |
| 2 | Delivery | GitHub naming rules, commit message, release tag, submission metadata helper | Done |
| 2 | Notification | Feishu text template + webhook request + audited send workflow | Done |
| 2 | CLI | Minimal parser and runnable module entrypoint | Done |
| 3 | Demo Layer | End-to-end script orchestration against real services | Pending external credentials |
| 3 | Real Integration | Live Wecreate and Feishu execution | Pending external credentials |

## Blockers

- Real execution still requires a running Wecreate service and a valid access token.
- Feishu delivery still requires a valid webhook URL.

## Immediate Demo Sequence

1. Load persona from `config/personas/example-agent.json`
2. Sync profile to Wecreate
3. Read hackathon detail
4. Read current enrollment
5. Create enrollment if missing
6. Request AI team matches
7. Create or join a team
8. Emit Feishu notification
9. Render audit timeline from JSONL
