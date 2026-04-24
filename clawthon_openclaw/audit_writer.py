from __future__ import annotations

import json
from pathlib import Path

from clawthon_openclaw.audit import AuditEvent


class JsonlAuditWriter:
    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)

    def write(self, event: AuditEvent) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
