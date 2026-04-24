from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WecreateClientConfig:
    base_url: str
    access_token: str | None = None

    def endpoint(self, path: str) -> str:
        base_url = self.base_url.rstrip("/")
        normalized_path = path if path.startswith("/") else f"/{path}"
        return f"{base_url}{normalized_path}"

    def auth_headers(self) -> dict[str, str]:
        if not self.access_token:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}


@dataclass(frozen=True)
class WecreateRequest:
    method: str
    url: str
    headers: dict[str, str]
    json_body: dict[str, object] | None = None


class WecreateClient:
    def __init__(self, config: WecreateClientConfig) -> None:
        self.config = config

    def list_hackathons(self) -> WecreateRequest:
        return WecreateRequest(
            method="GET",
            url=self.config.endpoint("/api/v1/hackathons"),
            headers=self.config.auth_headers(),
            json_body=None,
        )

    def read_hackathon_detail(self, *, hackathon_id: int) -> WecreateRequest:
        return WecreateRequest(
            method="GET",
            url=self.config.endpoint(f"/api/v1/hackathons/{hackathon_id}"),
            headers=self.config.auth_headers(),
            json_body=None,
        )

    def read_my_enrollment(self, *, hackathon_id: int) -> WecreateRequest:
        return WecreateRequest(
            method="GET",
            url=self.config.endpoint(f"/api/v1/enrollments/my/{hackathon_id}"),
            headers=self.config.auth_headers(),
            json_body=None,
        )

    def create_enrollment(self, *, hackathon_id: int) -> WecreateRequest:
        return WecreateRequest(
            method="POST",
            url=self.config.endpoint("/api/v1/enrollments/"),
            headers=self.config.auth_headers(),
            json_body={"hackathon_id": hackathon_id},
        )

    def create_team(
        self,
        *,
        hackathon_id: int,
        team_payload: dict[str, object],
    ) -> WecreateRequest:
        return WecreateRequest(
            method="POST",
            url=self.config.endpoint(f"/api/v1/teams?hackathon_id={hackathon_id}"),
            headers=self.config.auth_headers(),
            json_body=team_payload,
        )

    def join_team(self, *, team_id: int) -> WecreateRequest:
        return WecreateRequest(
            method="POST",
            url=self.config.endpoint(f"/api/v1/teams/{team_id}/join"),
            headers=self.config.auth_headers(),
            json_body=None,
        )

    def join_team_via_invite(self, *, invite_token: str) -> WecreateRequest:
        return WecreateRequest(
            method="POST",
            url=self.config.endpoint(f"/api/v1/teams/invite/{invite_token}/join"),
            headers=self.config.auth_headers(),
            json_body=None,
        )

    def create_submission(
        self,
        *,
        hackathon_id: int,
        team_id: int,
        payload: dict[str, object],
    ) -> WecreateRequest:
        return WecreateRequest(
            method="POST",
            url=self.config.endpoint(f"/api/v1/submissions?hackathon_id={hackathon_id}&team_id={team_id}"),
            headers=self.config.auth_headers(),
            json_body=payload,
        )

    def finalize_submission(self, *, submission_id: int) -> WecreateRequest:
        return WecreateRequest(
            method="POST",
            url=self.config.endpoint(f"/api/v1/submissions/{submission_id}/finalize"),
            headers=self.config.auth_headers(),
            json_body=None,
        )

    def team_match(self, *, hackathon_id: int, requirements: str) -> WecreateRequest:
        return WecreateRequest(
            method="POST",
            url=self.config.endpoint("/api/v1/ai/team-match"),
            headers=self.config.auth_headers(),
            json_body={
                "hackathon_id": hackathon_id,
                "requirements": requirements,
            },
        )

    def update_current_user(self, *, profile: dict[str, object]) -> WecreateRequest:
        return WecreateRequest(
            method="PUT",
            url=self.config.endpoint("/api/v1/users/me"),
            headers=self.config.auth_headers(),
            json_body=profile,
        )
