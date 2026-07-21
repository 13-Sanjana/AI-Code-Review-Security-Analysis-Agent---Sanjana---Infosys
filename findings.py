from dataclasses import dataclass

@dataclass
class Finding:
    rule: str
    severity: str
    line: int
    message: str
    recommendation: str