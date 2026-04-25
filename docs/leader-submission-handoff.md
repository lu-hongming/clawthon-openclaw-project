# Leader Submission Handoff

This handoff lets the leader-side agent create the Wecreate team draft without needing any member-side secrets.

## Current State

- Wecreate event: <https://wecreate.net.cn/events/2>
- Hackathon ID: `2`
- Team ID: `10`
- Repository: <https://github.com/lu-hongming/clawthon-openclaw-project>
- Public submissions check currently returns `[]`.
- Submission phase is `open`.
- Team submission writes require the team leader account.

## Required Leader Environment

The leader-side agent needs a valid team-leader JWT in environment only. Do not commit it.

```bash
export WECREATE_API_BASE_URL='https://wecreate.net.cn'
export WECREATE_ALLOWED_HACKATHON_IDS='2'
export WECREATE_API_BEARER_TOKEN='REPLACE_WITH_LEADER_JWT'
```

## Create Draft

Run this from the repository root after setting the leader JWT:

```bash
python3 skills/wecreate-hackathon-participant/scripts/wecreate_submission_api.py create \
  --hackathon-id 2 \
  --team-id 10 \
  --payload-file submission/wecreate-draft-payload.json
```

Expected result:

- A draft submission is created for hackathon `2`.
- The returned JSON contains the new `submission_id`.
- Do not finalize yet.

## Verify Draft

```bash
python3 skills/wecreate-hackathon-participant/scripts/wecreate_submission_api.py my-submissions \
  --hackathon-id 2
```

If the draft already exists, update it instead:

```bash
python3 skills/wecreate-hackathon-participant/scripts/wecreate_submission_api.py update \
  --hackathon-id 2 \
  --submission-id SUBMISSION_ID \
  --payload-file submission/wecreate-draft-payload.json
```

## Guardrails

- Do not use browser automation for this handoff.
- Do not finalize without an explicit final-submit instruction.
- Do not paste JWTs into Feishu, GitHub, Markdown, or logs.
- If Wecreate returns `403 仅队长可以提交作品`, the JWT is not from the team leader account.
