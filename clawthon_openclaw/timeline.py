from __future__ import annotations

import json
from pathlib import Path


def render_markdown_timeline(path: str | Path) -> str:
    timeline_path = Path(path)
    lines = timeline_path.read_text(encoding="utf-8").splitlines() if timeline_path.exists() else []
    events = [json.loads(line) for line in lines if line.strip()]

    output = ["# Audit Timeline", ""]
    for event in events:
        output.append(
            f"- `{event['timestamp']}` `{event['phase']}` `{event['action_name']}` `{event['status']}`"
        )
        output.append(f"  reason: {event['decision_reason']}")
        output.append(f"  output: {event['output_summary']}")
    return "\n".join(output) + ("\n" if output else "")

