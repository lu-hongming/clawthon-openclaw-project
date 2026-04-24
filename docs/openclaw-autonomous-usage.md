# OpenClaw Autonomous Usage

## Purpose

This is an API-first execution contract for an OpenClaw participant joining the production Wecreate Clawthon team invite.

Do not use browser automation. Use backend APIs only.

## Fixed Target

```yaml
workspace: /Users/haiy_qq/Desktop/比赛/SJTU OPENCLAW
api_base_url: https://wecreate.net.cn
hackathon_id: 2
event_url: https://wecreate.net.cn/events/2
invite_url: provided out of band
invite_token: provided out of band
participant_skill_dir: /Users/haiy_qq/Desktop/比赛/SJTU OPENCLAW/wecreate-hackathon-participant
submission_script: /Users/haiy_qq/Desktop/比赛/SJTU OPENCLAW/wecreate-hackathon-participant/scripts/wecreate_submission_api.py
```

## Required Human Inputs

OpenClaw may proceed without browser access, but phone verification still requires human input.

Required before authenticated calls:

- `WECREATE_LOGIN_PHONE`: a valid mainland China phone number.
- `WECREATE_PHONE_CODE`: the SMS verification code received on that phone.
- `WECREATE_API_BEARER_TOKEN`: optional existing JWT for the participant account.

If `WECREATE_API_BEARER_TOKEN` exists, skip SMS sending and code verification. If no token exists, both `WECREATE_LOGIN_PHONE` and `WECREATE_PHONE_CODE` are required. Do not guess or reuse a phone number from public invite metadata.

## Current Production Facts

Verified from production APIs on `2026-04-24`:

- The private team invite returns team `10`.
- Team name is `OpenClaw 冲冲冲！`.
- Team belongs to `hackathon_id=2`.
- Team has `active_member_count=2` and is not full.
- Team `recruitment_status` is currently `closed`.
- Backend join logic rejects closed recruitment with `409 团队已完成招募`.
- The participant phone authenticates as user `7`, nickname `亥一`.
- User `7` is already enrolled in hackathon `2` with status `approved`.
- User `7` is already an active member of team `10`.
- Hackathon `2` currently has `submission_phase_status=open`.
- Current participant has no existing submission for hackathon `2`.
- Production draft creation with user `7` and `team_id=10` returns `403 仅队长可以提交作品`.

Therefore, joining is already complete for this participant. Do not call the invite join endpoint again unless membership disappears.

## Non-Negotiable Rules

- Use `https://wecreate.net.cn` only.
- Use `hackathon_id=2` only.
- Use only the private invite token supplied out of band.
- Do not use browser automation.
- Do not call organizer or judge endpoints.
- Do not invent a phone number or SMS code.
- Do not create, update, or finalize submissions unless submission phase is `open`.
- Do not finalize a submission unless the user explicitly asks for final submission.

## Step 1: Read Invite Metadata

```bash
curl -sS https://wecreate.net.cn/api/v1/teams/invite/$WECREATE_INVITE_TOKEN
```

Success conditions:

- Response JSON contains `hackathon_id: 2`.
- Response JSON contains `team.id`.

Decision rules:

- If the authenticated user is already in `team.members`, treat join as complete even when recruitment is closed.
- If `team.recruitment_status != "open"` and the authenticated user is not already a member, report `team_recruitment_closed`.
- If `is_full == true`, stop and report `team_full`.

## Step 2: Read Hackathon Metadata

```bash
curl -sS https://wecreate.net.cn/api/v1/hackathons/2
```

Success conditions:

- Response JSON contains `id: 2`.
- `registration_phase_status` is `open`.

Decision rules:

- If registration is not open, stop and report `registration_not_open`.
- Record `submission_phase_status`; if it is not `open`, skip submission create/update/finalize later.

## Step 3: Send Phone Verification Code

Skip this step if `WECREATE_API_BEARER_TOKEN` already exists.

Only run this step if `WECREATE_LOGIN_PHONE` is present and no bearer token exists.

```bash
curl -sS -X POST https://wecreate.net.cn/api/v1/auth/phone/send-code \
  -H 'Content-Type: application/json' \
  -d "{\"phone\":\"$WECREATE_LOGIN_PHONE\"}"
```

Success conditions:

- Response JSON contains `message: 验证码已发送`.

Decision rules:

- If this returns `429`, stop and report the cooldown.
- If this returns `502`, SMS provider failed; stop and report the provider error.
- Wait for the user to provide `WECREATE_PHONE_CODE`.

## Step 4: Verify Phone Code And Capture JWT

Skip this step if `WECREATE_API_BEARER_TOKEN` already exists.

Only run this step if both `WECREATE_LOGIN_PHONE` and `WECREATE_PHONE_CODE` are present and no bearer token exists.

```bash
curl -sS -X POST https://wecreate.net.cn/api/v1/auth/phone/verify \
  -H 'Content-Type: application/json' \
  -d "{\"phone\":\"$WECREATE_LOGIN_PHONE\",\"code\":\"$WECREATE_PHONE_CODE\"}"
```

Success conditions:

- Response JSON contains `access_token`.

Required action:

- Export the token as `WECREATE_API_BEARER_TOKEN`.

```bash
export WECREATE_API_BASE_URL='https://wecreate.net.cn'
export WECREATE_ALLOWED_HACKATHON_IDS='2'
export WECREATE_API_BEARER_TOKEN='REPLACE_WITH_ACCESS_TOKEN'
```

Decision rules:

- If verification returns `400 验证码无效或已过期`, stop and request a new SMS code.
- If the token is captured, proceed to Step 5.

## Step 5: Read Current Enrollment

```bash
curl -sS https://wecreate.net.cn/api/v1/enrollments/my/2 \
  -H "Authorization: Bearer $WECREATE_API_BEARER_TOKEN"
```

Decision rules:

- If status is `200`, record the enrollment status and continue to Step 7.
- If status is `404`, run Step 6.
- If status is `401` or `403`, stop and report `invalid_bearer_token`.

## Step 6: Register For Hackathon

Use this payload for a participant looking for a team.

```bash
curl -sS -X POST https://wecreate.net.cn/api/v1/enrollments/register/2 \
  -H "Authorization: Bearer $WECREATE_API_BEARER_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "default_field_values": {
      "team_status": "寻找团队中",
      "terms_of_service": true
    },
    "custom_field_values": {
      "personal_description": "OpenClaw autonomous participant joining the Clawthon team through the Wecreate API.",
      "personal_tags": ["OpenClaw", "Agent", "Backend"]
    }
  }'
```

Success conditions:

- Response JSON contains `hackathon_id: 2`.
- Enrollment status may be `pending`; this is acceptable for invite join because pending enrollment creates a pending team membership.

Decision rules:

- If the API says the user is already enrolled, continue to Step 7.
- If required fields changed, read `GET /api/v1/hackathons/2/registration-form`, adapt the payload, then retry.

## Step 7: Join Team Via Invite

Before joining, re-read invite metadata.

If the authenticated user is already in `team.members`, skip this step and report `already_member`.

If the authenticated user is not already a member and `team.recruitment_status` is still `closed`, stop and report `team_recruitment_closed`.

```bash
curl -sS -X POST https://wecreate.net.cn/api/v1/teams/invite/$WECREATE_INVITE_TOKEN/join \
  -H "Authorization: Bearer $WECREATE_API_BEARER_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Success conditions:

- Response JSON contains `team_id: 10`.
- Response JSON contains `status`.

Decision rules:

- `status: active` means the participant joined successfully.
- `status: pending_approval` means the join request was submitted and will become active after enrollment approval.
- `400 Already a member of this team` means success-equivalent.
- `409 团队已完成招募` means the team leader must reopen recruitment.

## Step 8: Inspect Submission Form Only

Run only after JWT is available.

```bash
python3 /Users/haiy_qq/Desktop/比赛/SJTU\ OPENCLAW/wecreate-hackathon-participant/scripts/wecreate_submission_api.py \
  form-config \
  --hackathon-id 2
```

Required default fields currently include:

- `title`
- `cover_image`
- `tagline`
- `description`

## Step 9: Inspect Current Submissions

Run only after JWT is available.

```bash
export WECREATE_API_BASE_URL='https://wecreate.net.cn'
export WECREATE_ALLOWED_HACKATHON_IDS='2'
python3 /Users/haiy_qq/Desktop/比赛/SJTU\ OPENCLAW/wecreate-hackathon-participant/scripts/wecreate_submission_api.py \
  my-submissions \
  --hackathon-id 2
```

If the response is an empty array, report `submission_state=no_submission`.

## Step 10: Draft Submission Guardrail

Do not create or update a production submission unless the user provides real project content.

Required content before creating a draft:

- project title
- public cover image URL
- tagline
- project description

Recommended optional content:

- repository URL
- demo URL

For team hackathon submissions, include `--team-id 10`. The current authenticated user `7` is not the team leader, and production has confirmed `403 仅队长可以提交作品` for draft creation. To write a submission, use the team leader JWT or transfer team leadership to user `7`.

## Final Reporting Format

Return one JSON object:

```json
{
  "event_url": "https://wecreate.net.cn/events/2",
  "invite_url": "provided_out_of_band",
  "hackathon_id": 2,
  "team_id": 10,
  "invite_read": "success|failed",
  "team_recruitment_status": "open|closed|unknown",
  "hackathon_read": "success|failed",
  "phone_code_sent": "success|failed|skipped",
  "jwt_state": "ready|missing_phone|missing_code|invalid_code|failed",
  "enrollment_state": "already_enrolled|registered|missing|failed|skipped",
  "join_state": "joined|pending_approval|already_member|blocked|failed|skipped",
  "submission_phase_status": "open|not_started|closed|unknown",
  "submission_state": "no_submission|draft_exists|submitted_exists|unknown",
  "blocker": null,
  "notes": []
}
```
