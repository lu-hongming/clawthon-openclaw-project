# Wecreate participant submission workflow

Use this reference with the skill helper at `{baseDir}/scripts/wecreate_submission_api.py`.

## Required environment

The skill expects these variables to exist before OpenClaw starts:

- `WECREATE_API_BASE_URL`
  Example: `https://wecreate.example.com`
- `WECREATE_API_BEARER_TOKEN`
  Bearer token for the participant account OpenClaw should act as.
- `WECREATE_ALLOWED_HACKATHON_IDS`
  Comma- or space-separated allowlist such as `42, 108`.

The helper script refuses requests outside the allowlist.

## Recommended participant flow

1. Read form config for the target hackathon.
2. Read the current user's submission list for that hackathon.
3. Create a draft if no submission exists yet, otherwise update the existing draft.
4. Finalize only when the user explicitly asks to submit.

## Endpoint map

These routes are participant-safe and useful for this skill:

- `GET /api/v1/submission-fields/hackathons/{hackathon_id}/form-config`
  Preferred form discovery endpoint. This route exists in the backend even though it is not present in the extracted `api.md`.
- `GET /api/v1/submissions/me`
  Read the authenticated user's submissions. Filter client-side by hackathon when needed.
- `GET /api/v1/submissions?hackathon_id=...`
  Read visible submissions for one hackathon.
- `GET /api/v1/submissions/{submission_id}`
  Read one submission.
- `POST /api/v1/submissions?hackathon_id=...`
  Create a draft submission.
- `PATCH /api/v1/submissions/{submission_id}`
  Update a draft submission.
- `POST /api/v1/submissions/{submission_id}/finalize`
  Finalize a draft into a submitted project.

Avoid organizer-only or retired submission-field mutation endpoints.

## Payload shape

Create and update both use the `SubmissionCreate` request shape:

```json
{
  "default_field_values": {
    "title": "Project Atlas",
    "cover_image": "https://cdn.example.com/atlas-cover.png",
    "tagline": "AI copilot for field teams",
    "description": "Atlas helps distributed teams capture, search, and verify site notes.",
    "demo_url": "https://atlas.example.com/demo",
    "repo_url": "https://github.com/example/atlas"
  },
  "custom_field_values": {
    "tech_stack": ["FastAPI", "React", "Postgres"],
    "deployment_stage": "beta",
    "team_size": 3
  }
}
```

## Field typing rules

Use the resolved field types from `form-config`:

- `text`, `textarea`: send a string
- `image`, `url`: send a valid `http` or `https` URL string
- `number`: send a number
- `single_select`: send one allowed string option
- `multi_select`: send an array of allowed string options

Important details from the backend:

- Only enabled default fields may be sent. Disabled default keys cause a `400`.
- Required fields must be present and non-empty.
- `description` may be plain text.
- Team hackathons require `team_id` on create and may reject writes unless the authenticated user is the team leader.

## Helper command examples

Inspect the form:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py form-config --hackathon-id 42
```

Read current submissions:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py my-submissions --hackathon-id 42
```

Create a draft:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py create \
  --hackathon-id 42 \
  --title "Project Atlas" \
  --cover-image "https://cdn.example.com/atlas-cover.png"
```

Update with custom fields:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py update \
  --hackathon-id 42 \
  --submission-id 108 \
  --custom-field tech_stack='["FastAPI","React","Postgres"]' \
  --custom-field deployment_stage='"beta"'
```

Finalize after explicit confirmation:

```bash
python3 {baseDir}/scripts/wecreate_submission_api.py finalize \
  --hackathon-id 42 \
  --submission-id 108
```

## Raw OpenAPI extract

The user-provided extracted OpenAPI lives at `{baseDir}/../../api.md`. Read that file when you need the raw route declarations. Use this reference first for operational guidance.
