# Clawthon OpenClaw Side Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the minimum viable OpenClaw-side capability loop for Clawthon so agents can autonomously join, team up, collaborate, submit, and leave auditable traces on top of Wecreate.

**Architecture:** Wecreate remains the hackathon platform and workflow host, while OpenClaw acts as the autonomous participant runtime. The first milestone is not full platform reconstruction, but a stable agent-facing loop: persona sync, registration and teaming, collaboration tooling, submission delivery, and structured audit logging. Platform changes should be minimized and driven by explicit API gaps rather than broad redesign.

**Tech Stack:** OpenClaw skills and orchestration, Wecreate (FastAPI + React), GitHub integration, Feishu integration, structured event logging

---

## 1. Context And Boundary

### Existing platform capabilities confirmed

Based on the current Wecreate repository and the competition proposal, the platform already has these foundations:

- Hackathon lifecycle management
- Enrollment and participant records
- Team creation and team membership
- Submission workflow
- AI-assisted team matching
- Notification center and basic AI endpoints

Relevant references:

- `/Users/haiy_qq/Desktop/比赛/SJTU OPENCLAW/Wecreate/README.md`
- `/Users/haiy_qq/Desktop/比赛/SJTU OPENCLAW/Wecreate/docs/TECHNICAL_REFERENCE.md`
- `/Users/haiy_qq/Desktop/比赛/SJTU OPENCLAW/Wecreate/backend/app/models/user.py`
- `/Users/haiy_qq/Desktop/比赛/SJTU OPENCLAW/Wecreate/backend/app/api/v1/endpoints/teams.py`
- `/Users/haiy_qq/Desktop/比赛/SJTU OPENCLAW/Wecreate/backend/app/api/v1/endpoints/ai.py`

### Missing capability loop for the competition

The proposal requires a stronger agent-native workflow that is not fully present yet:

- Agent identity and differentiated persona profile
- OpenClaw-native skill packs for the hackathon lifecycle
- Feishu collaboration automation
- GitHub development trace management
- Structured behavior audit and replay data
- Agent-facing execution flow rather than only human-facing web pages

### Scope of responsibility for the OpenClaw side

This plan assumes the OpenClaw side is primarily responsible for:

- Defining the agent persona structure
- Building the agent-facing skill packages
- Driving autonomous decisions and API invocation
- Integrating GitHub and Feishu from the agent workflow
- Emitting structured behavior logs
- Raising concrete API dependency requests to the Wecreate side

This plan does not assume OpenClaw owns the whole Wecreate platform UI or its full backend redesign.

---

## 2. Delivery Strategy

### Stage goal

The first shippable milestone is a minimum closed loop:

1. Agent profile is initialized and synced
2. Agent enrolls in a hackathon
3. Agent searches for teammates and joins or forms a team
4. Agent collaborates through GitHub and optional Feishu notifications
5. Agent submits the project
6. All key decisions and tool calls are logged in a structured format

### Priority order

1. Environment and API understanding
2. Persona and identity mapping
3. Registration and teaming loop
4. GitHub delivery flow
5. Feishu collaboration notifications
6. Audit logging and replay support
7. End-to-end demo hardening

### Design principle

Build the narrowest loop that can be demonstrated end to end. Anything not required for the first demo should be treated as optional unless it blocks the loop.

---

## 3. Workstreams

### Workstream A: Local environment and joint debugging setup

**Objective:** Make Wecreate callable and predictable from the OpenClaw side.

**Outputs:**

- A local Wecreate environment that can be started reliably
- Seed data for one demo hackathon
- A stable set of test users or agent accounts
- A local integration note for endpoints, tokens, and sample IDs

**Tasks:**

1. Run Wecreate frontend and backend locally.
2. Seed or create one dedicated Clawthon event for debugging.
3. Prepare 2 to 4 test identities with different skills and personalities.
4. Verify the key APIs needed by OpenClaw:
   - hackathon read
   - enrollment create/read
   - team list/create/join
   - AI team match
   - submission create/update
5. Record successful request examples for later skill implementation.

**Done criteria:**

- You can manually complete the core event flow with test accounts.
- OpenClaw development no longer depends on guessing request shapes.

### Workstream B: Agent identity and persona model

**Objective:** Turn OpenClaw agents into first-class competition participants rather than generic users.

**Outputs:**

- A persona config schema for each agent
- A mapping rule from OpenClaw persona to Wecreate user fields
- A short list of missing platform fields, if any

**Recommended persona fields:**

- `agent_name`
- `role_preference`
- `personality_tags`
- `execution_style`
- `risk_boundary`
- `memory_summary`
- `skills`
- `collaboration_preference`
- `external_tool_policy`

**Tasks:**

1. Define the local persona configuration structure used by OpenClaw.
2. Map existing fields to Wecreate user fields such as `skills`, `personality`, and `bio`.
3. Identify the minimum missing fields needed for public agent profile display.
4. Decide the authentication pattern:
   - reuse normal user login
   - or define service-account style access for agents
5. Document the sync rules between local agent memory and platform profile fields.

**Done criteria:**

- Each demo agent can be initialized from config.
- Its platform-visible profile can be reproduced from OpenClaw state.

### Workstream C: OpenClaw skill package design

**Objective:** Avoid one oversized skill. Split the hackathon workflow into clear agent capabilities.

**Outputs:**

- Skill package structure
- Prompt contracts and tool boundaries for each skill
- Shared context format between skills

**Recommended skill split:**

- `hackathon_profile`
  - sync persona
  - inspect current registration identity
- `hackathon_teaming`
  - enroll in event
  - inspect candidates
  - invite or join teammates
  - confirm role coverage
- `hackathon_delivery`
  - bind repo
  - follow branch and commit conventions
  - prepare submission payload
- `hackathon_audit`
  - emit structured logs
  - create replayable event traces
  - summarize decisions

**Tasks:**

1. Define the responsibility and inputs for each skill.
2. Define shared identifiers carried across the flow:
   - `hackathon_id`
   - `agent_id`
   - `team_id`
   - `project_id`
   - `trace_id`
3. Standardize success and failure outputs for each skill.
4. Add retry and fallback rules for external API failures.

**Done criteria:**

- A new engineer can understand which skill owns which action.
- The end-to-end flow can be composed from these four skill packages.

### Workstream D: Registration and autonomous teaming loop

**Objective:** Build the first real autonomous competition behavior.

**Outputs:**

- Agent enrollment flow
- Candidate discovery and ranking flow
- Invite, join, accept, or fallback decision logic
- Team role coverage tracking

**Tasks:**

1. Fetch event and enrollment status.
2. Enroll the agent if not already enrolled.
3. Retrieve available teammates or use the AI team match endpoint as ranking assistance.
4. Evaluate teammates based on:
   - role complement
   - persona compatibility
   - skills coverage
   - remaining team gaps
5. Generate invite or join decisions with explicit reasoning.
6. Persist chosen team context into agent memory and audit logs.

**Open platform dependencies likely needed:**

- Clear candidate discovery endpoint or a reusable participant listing endpoint
- Public profile summary fields for agent comparison
- Team gap visibility or role coverage metadata
- Invitation status visibility if the platform supports invitation workflow

**Done criteria:**

- Two or more agents can autonomously form or join a team with traceable reasoning.

### Workstream E: GitHub collaboration loop

**Objective:** Make the agent workflow produce credible development artifacts rather than only chat traces.

**Outputs:**

- Repo binding conventions
- Branch naming rule
- Commit message rule
- README or submission template guidance
- Release artifact checklist

**Tasks:**

1. Define how a team repo is associated with a Clawthon project.
2. Establish minimum conventions:
   - branch naming
   - commit prefixes
   - README sections
   - release tag format
3. Let agents update delivery metadata needed by the platform:
   - repo URL
   - demo URL
   - video URL
   - release tag
4. Capture GitHub activity into the audit log with timestamps and references.

**Recommended first milestone:**

- Focus on repo binding and submission metadata first.
- Defer advanced contribution analytics unless required by judging.

**Done criteria:**

- A demo team can submit a real repo-backed project with consistent metadata.

### Workstream F: Feishu collaboration notifications

**Objective:** Show that agents can collaborate through an external channel without overbuilding the first version.

**Outputs:**

- Feishu event sync design
- Minimal notification templates
- Optional team chat creation flow

**Recommended first milestone events:**

- team formed
- task assigned
- submission reminder
- submission completed
- judging or result notice

**Tasks:**

1. Decide whether Feishu is required in v1 as a true chat workspace or only as notification sync.
2. Implement event templates for key hackathon states.
3. Add event emission from OpenClaw actions and platform callbacks where possible.
4. Record message IDs and timestamps into the audit log.

**Risk control:**

- Treat full conversational Feishu integration as optional unless it is required for the demo.
- Notification sync is enough for the first usable milestone.

**Done criteria:**

- Key events can be pushed to Feishu and linked back to the agent trace.

### Workstream G: Structured audit logging and replay

**Objective:** Preserve the research value of the project from day one.

**Outputs:**

- A structured event schema
- Persistent trace records
- A minimal replay or summarized timeline output

**Minimum schema recommendation:**

- `trace_id`
- `timestamp`
- `agent_id`
- `phase`
- `skill_name`
- `action_name`
- `target_type`
- `target_id`
- `input_summary`
- `output_summary`
- `decision_reason`
- `external_refs`
- `status`

**Tasks:**

1. Define a single structured logging schema before broad implementation starts.
2. Make all OpenClaw hackathon skills emit events in that schema.
3. Add references to platform objects and GitHub or Feishu artifacts.
4. Produce one replay-friendly view:
   - chronological JSON
   - or markdown timeline
   - or a simple UI page later

**Done criteria:**

- Every important action in the demo can be reconstructed without reading raw terminal history.

### Workstream H: Demo scenario and acceptance test

**Objective:** Convert engineering work into a stable competition demonstration.

**Outputs:**

- One successful end-to-end demo script
- One fallback or failure-recovery demo script
- A checklist for live demo readiness

**Recommended demo script:**

1. Agent syncs profile
2. Agent enrolls in Clawthon
3. Agent finds teammates
4. Team confirms roles
5. Agent works against GitHub repo
6. Agent submits project
7. Judge can inspect outcome and behavior trace

**Tasks:**

1. Script the happy path with fixed sample data.
2. Script one failure path such as failed match or missing teammate.
3. Verify all external references exist and are clickable or inspectable.
4. Prepare a fallback local-only demo mode if online dependencies fail.

**Done criteria:**

- The full demo can be repeated with minimal manual intervention.

---

## 4. API Dependency List For The Wecreate Side

This is the platform-side contract that should be confirmed early with the other developer:

### Already likely usable

- hackathon read APIs
- enrollment APIs
- team create and join APIs
- AI team match API
- submission APIs

### Likely missing or needing refinement

- public agent profile summary for comparison
- team role gap visibility
- explicit invitation workflow for agent-to-agent teaming
- agent-friendly auth or token strategy
- structured webhook or event callback hooks
- project binding fields for GitHub release or trace metadata
- audit-facing endpoints if logs must be pushed platform-side

### Coordination rule

Every requested platform change should include:

- why OpenClaw needs it
- whether there is an existing workaround
- whether it is blocking the minimum demo
- the exact request and response shape preferred

---

## 5. Recommended Timeline

### Day 1

- Run Wecreate locally
- confirm key APIs
- define minimum closed loop
- define shared IDs and trace strategy

### Day 2

- finalize persona config
- map persona to platform fields
- scaffold the four OpenClaw skills

### Day 3

- implement enrollment flow
- implement teammate discovery and ranking
- implement join or create team flow

### Day 4

- implement GitHub repo binding and delivery conventions
- wire submission payload generation

### Day 5

- implement Feishu key-event sync
- implement structured audit logging end to end

### Day 6

- end-to-end debugging
- fix contract gaps
- prepare demo script and fallback path

### Day 7

- harden stability
- polish docs
- prepare presentation and defense materials

---

## 6. Risks And Control Measures

### Risk 1: Existing APIs are human-page oriented, not agent oriented

**Control:** Confirm request and response shapes early and write wrapper adapters on the OpenClaw side instead of assuming direct reuse is enough.

### Risk 2: Feishu and GitHub integration expand too fast

**Control:** Keep the first version to repo binding plus key event notifications. Defer rich collaboration automation until after the main loop works.

### Risk 3: Audit logging is treated as an afterthought

**Control:** Freeze the event schema before implementing broad workflow logic.

### Risk 4: Demo depends on too many online services

**Control:** Prepare a local or mocked fallback path for at least one full end-to-end demo.

---

## 7. Immediate Next Actions

These are the next three actions with the best leverage:

1. Confirm the minimum OpenClaw-facing API list with the Wecreate developer.
2. Finalize the agent persona schema and mapping rules.
3. Finalize the structured audit log schema before skill implementation starts.

---

## 8. Acceptance Standard

The OpenClaw side is considered ready for the competition demo when all of the following are true:

- At least two agent identities can be initialized with differentiated personas.
- An agent can enroll in the event and inspect candidate teammates.
- Agents can autonomously team up or form a team with traceable reasons.
- The team can bind a GitHub repo and prepare a valid submission.
- Key collaboration or status events can reach Feishu or an equivalent notification path.
- Every critical action is recorded in a structured trace that can be replayed or summarized.

---

## 9. Notes

- The first version should optimize for a convincing and reproducible demo, not complete platform generalization.
- Platform changes should be minimal and justified by the agent loop.
- If time becomes tight, cut in this order:
  1. rich Feishu chat behavior
  2. advanced GitHub analytics
  3. complex replay UI
  4. non-blocking profile embellishments
