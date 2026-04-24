# OpenClaw GitHub Collaboration

## Bound GitHub Identity

OpenClaw can use the local GitHub CLI authentication.

- GitHub user: `Hai-qq`
- Profile: `https://github.com/Hai-qq`
- Auth source: local `gh` keychain login
- Available scopes: `repo`, `workflow`, `read:org`, `gist`

Do not write the GitHub token into repo files. Use `gh` commands so the token stays in the system credential store.

## Current Wecreate Team

- Hackathon ID: `2`
- Team ID: `10`
- Team name: `OpenClaw 冲冲冲！`
- Member Wecreate user: `user_id=7`, nickname `亥一`
- Member GitHub user: `Hai-qq`
- Team leader Wecreate user: `user_id=2`, nickname `陆泓铭`

## Collaboration Model

The Wecreate submission and the GitHub repository are separate control planes.

Wecreate:

- Only the team leader can create, update, and finalize the team submission.
- Member user `7` can read team context but cannot submit for team `10`.

GitHub:

- The repository owner or admin invites collaborators.
- Each OpenClaw agent works through its own GitHub identity.
- Work should happen through branches and pull requests.

## Leader-Owned Repository Flow

Use this when the leader owns the repository.

1. Leader agent creates or selects the repository.
2. Leader agent invites `Hai-qq` as collaborator.
3. Member agent accepts the repository invitation.
4. Member agent creates a branch named `agent/member-openclaw-workflow`.
5. Leader agent creates a branch named `agent/leader-submission`.
6. Agents coordinate through issues and pull requests.
7. Leader agent merges approved PRs.
8. Leader agent writes the final `repo_url` into the Wecreate submission.

Leader invite command:

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/OWNER/REPO/collaborators/Hai-qq \
  -f permission=push
```

Member accept invitation flow:

```bash
gh api /user/repository_invitations
gh api \
  --method PATCH \
  /user/repository_invitations/INVITATION_ID
```

## Member-Owned Repository Flow

Use this when `Hai-qq` creates the repository.

1. Member agent creates the repository under `Hai-qq`.
2. Member agent invites the leader GitHub username as collaborator.
3. Leader accepts the invitation.
4. Leader remains responsible for Wecreate submission because Wecreate requires the team leader account.

Create repository:

```bash
gh repo create Hai-qq/clawthon-openclaw-team-10 \
  --private \
  --description "OpenClaw agent-native Clawthon project" \
  --clone
```

Invite leader:

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/Hai-qq/clawthon-openclaw-team-10/collaborators/LEADER_GITHUB_USERNAME \
  -f permission=push
```

## Branch Rules

- `main`: stable project state only.
- `agent/leader-submission`: Wecreate submission copy, final polish, release metadata.
- `agent/member-openclaw-workflow`: OpenClaw API workflow, automation, docs, tests.
- `fix/*`: targeted fixes.

## Commit Format

Use short role-prefixed commit messages:

```text
leader: update submission metadata
member: add openclaw api workflow docs
member: validate github collaboration flow
```

## Current Blockers

- Target repository is `https://github.com/lu-hongming/clawthon-openclaw-project`.
- The repository was public and empty when first checked.
- GitHub user `Hai-qq` has accepted the collaborator invitation and GitHub reports `push=true`.
- The local clone is `clawthon-openclaw-project`.
- Empty-repository fork blocking is resolved once the initial commit is pushed.
- Wecreate submission still requires the leader JWT or a leadership transfer.

## Current Target Repository

- Owner/repo: `lu-hongming/clawthon-openclaw-project`
- URL: `https://github.com/lu-hongming/clawthon-openclaw-project`
- Visibility: public
- Current `Hai-qq` permission: push
- Default branch: `main`

The collaborator invitation has already been accepted. New work can proceed through branches and pull requests.
