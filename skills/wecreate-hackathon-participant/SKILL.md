---
name: wecreate-hackathon-participant
description: Act as a Wecreate hackathon participant for allowed hackathons by reading submission requirements and using the submissions API to inspect, create, edit, and finalize the current user's submission. Use when the user wants to draft a project entry, update a saved draft, inspect submission status, or submit a final project for a specific hackathon.
metadata: {"openclaw":{"emoji":"🏁","requires":{"bins":["python3"],"env":["WECREATE_API_BASE_URL","WECREATE_API_BEARER_TOKEN","WECREATE_ALLOWED_HACKATHON_IDS"]}}}
---

# Wecreate Hackathon Participant

Use this skill to manage hackathon submissions as an authenticated participant. Prefer the bundled helper script over handwritten `curl` because it handles bearer auth, hackathon allowlisting, and payload shaping.

## Workflow

1. Make the hackathon ID explicit. Do not guess across hackathons.
2. Read the form config first:
   `python3 {baseDir}/scripts/wecreate_submission_api.py form-config --hackathon-id 42`
3. Inspect the current participant state:
   `python3 {baseDir}/scripts/wecreate_submission_api.py my-submissions --hackathon-id 42`
4. Create or update a draft submission with only the enabled default fields plus any custom fields.
5. Finalize only when the user explicitly asks to submit the project. Saving a draft and finalizing are different operations.

## Guardrails

- Stay within `WECREATE_ALLOWED_HACKATHON_IDS`. The helper script rejects other hackathons.
- Use only participant-safe APIs. Do not call judging, organizer, or retired submission-field mutation endpoints.
- Prefer `form-config` over raw custom field definitions. It tells you which default fields are enabled and required for the target hackathon.
- Send only enabled default fields. The API rejects disabled default keys.
- Treat `description` as plain text unless the user explicitly asks to preserve editor-specific JSON.
- For team hackathons, create, update, and finalize may fail unless the authenticated user is the team leader. Surface the server error instead of guessing a workaround.
- For update or finalize, identify the submission ID first from `my-submissions` unless the user already gave it.

## Helper Commands

Inspect the active submission form:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py form-config --hackathon-id 42
```

List the current user's submissions, filtered to one hackathon:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py my-submissions --hackathon-id 42
```

Create a draft with common default fields:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py create \
  --hackathon-id 42 \
  --title "Project Atlas" \
  --cover-image "https://cdn.example.com/atlas-cover.png" \
  --tagline "AI copilot for field teams" \
  --description "Atlas helps distributed teams capture, search, and verify site notes." \
  --demo-url "https://atlas.example.com/demo" \
  --repo-url "https://github.com/example/atlas"
```

Create or update custom fields with JSON-capable values:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py update \
  --hackathon-id 42 \
  --submission-id 108 \
  --custom-field tech_stack='["FastAPI","React","Postgres"]' \
  --custom-field deployment_stage='"beta"'
```

Use a payload file for more complex edits:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py update \
  --hackathon-id 42 \
  --submission-id 108 \
  --payload-file /tmp/wecreate-submission.json
```

Finalize the submission after the user explicitly confirms:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py finalize \
  --hackathon-id 42 \
  --submission-id 108
```

## References

- Read `{baseDir}/references/participant-api-workflow.md` for payload examples, field typing rules, and endpoint notes.
- The raw extracted OpenAPI lives at `{baseDir}/../../api.md`.
