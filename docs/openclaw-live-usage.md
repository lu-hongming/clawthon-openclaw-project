# OpenClaw Live Usage

## Ready-to-use local environments

- Organizer env: `config/openclaw.organizer.env.local`
- Participant env: `config/openclaw.participant.env.local`
- Participant 2 env: `config/openclaw.participant2.env.local`

## Verified local Wecreate backend

- Base URL: `http://127.0.0.1:8010`

## Verified participant account

- Email: `openclaw.player@wecreate.net.cn`
- Username: `openclaw_player`
- Password: `player123`

## Verified second participant account

- Email: `openclaw.dev2@wecreate.net.cn`
- Username: `openclaw_dev2`
- Password: `dev2123`

## Verified working hackathon

- Hackathon ID: `1`
- Title: `AI 创新应用黑客松`

## Verified working team

- Team ID: `33`
- Team Name: `OpenClaw Builders`
- Invite Token: `m_lsWUs9DgYDAR8wFqMZ_uB1`
- Member Count: `2`

## Verified working submission

- Submission ID: `34`
- Submission Status: `submitted`
- Repo URL: `https://github.com/lu-hongming/Wecreate`
- Demo URL: `https://demo.example.com/openclaw-builders`

## Commands

### Sync participant profile

```bash
/opt/homebrew/bin/python3.13 -m clawthon_openclaw \
  --env-file config/openclaw.participant.env.local \
  sync-profile \
  --persona config/personas/example-agent.json
```

### Check current enrollment

```bash
/opt/homebrew/bin/python3.13 -m clawthon_openclaw \
  --env-file config/openclaw.participant.env.local \
  my-enrollment \
  --hackathon-id 1
```

### Run the team-start flow

```bash
/opt/homebrew/bin/python3.13 -m clawthon_openclaw \
  --env-file config/openclaw.participant.env.local \
  auto-team \
  --hackathon-id 1 \
  --requirements "Need backend and demo partner for AI hackathon project" \
  --team-name "OpenClaw Builders" \
  --team-description "Autonomous OpenClaw team for Clawthon delivery"
```

### Read audit timeline

```bash
/opt/homebrew/bin/python3.13 -m clawthon_openclaw \
  --env-file config/openclaw.participant.env.local \
  timeline \
  --audit-path output/audit/participant-demo.jsonl
```

### Join the verified team with the second participant

```bash
/opt/homebrew/bin/python3.13 -m clawthon_openclaw \
  --env-file config/openclaw.participant2.env.local \
  join-team \
  --team-id 33
```

### Submit and finalize a project delivery

```bash
/opt/homebrew/bin/python3.13 -m clawthon_openclaw \
  --env-file config/openclaw.participant.env.local \
  submit-delivery \
  --hackathon-id 1 \
  --team-id 33 \
  --title "OpenClaw Builders" \
  --tagline "Autonomous teaming and delivery for Clawthon" \
  --cover-image "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80" \
  --repo-url "https://github.com/lu-hongming/Wecreate" \
  --demo-url "https://demo.example.com/openclaw-builders" \
  --video-url "https://video.example.com/openclaw-builders" \
  --release-tag "clawthon-demo-v1" \
  --description "OpenClaw agents coordinate team formation, platform enrollment, and delivery submission on top of the Wecreate hackathon stack." \
  --ai-capability "Agent 工作流" \
  --ai-capability "多模态" \
  --inference-stack "OpenAI API + OpenClaw runtime" \
  --finalize
```

## Notes

- Team matching currently returns zero candidates for the chosen seeded scenario, but the endpoint is live and callable.
- Team creation, second-member join, and submission finalization are all verified end to end on the local backend.
- The chosen demo activity required manually opening the submission phase in the local seed database before submission testing.
- Feishu is still pending a real webhook URL.
