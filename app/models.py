
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlanStep:
    step_id: int
    description: str
    tool_name: str


@dataclass
class ToolResult:
    tool_name: str
    success: bool
    data: Any = None
    error: str | None = None


@dataclass
class AgentState:
    goal: str
    plan: list[PlanStep] = field(default_factory=list)
    results: list[ToolResult] = field(default_factory=list)
    failures: list[dict] = field(default_factory=list)
    status: str = "initialized"
