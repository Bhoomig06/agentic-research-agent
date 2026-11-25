
from app.models import PlanStep


def create_plan(goal: str) -> list[PlanStep]:
    """
    Create a goal-aware execution plan using local rules.

    The planner identifies the type of task from keywords
    and selects relevant tools without requiring an API key.
    """

    print("\n[PLANNER] Analyzing user goal...")

    normalized_goal = goal.lower()

    plan = []

    # Research-related goals
    research_keywords = [
        "research",
        "latest",
        "trends",
        "developments",
        "information",
        "compare",
        "analysis",
        "find"
    ]

    if any(keyword in normalized_goal for keyword in research_keywords):

        print("[PLANNER] Research task identified.")

        plan.append(
            PlanStep(
                step_id=len(plan) + 1,
                description="Search for relevant information",
                tool_name="web_search"
            )
        )

        plan.append(
            PlanStep(
                step_id=len(plan) + 1,
                description="Fetch the first relevant source",
                tool_name="fetch_url"
            )
        )

        plan.append(
            PlanStep(
                step_id=len(plan) + 1,
                description="Fetch another relevant source",
                tool_name="fetch_url"
            )
        )

    # Calculation-related goals
    calculation_keywords = [
        "calculate",
        "percentage",
        "average",
        "total",
        "ratio",
        "score"
    ]

    if any(keyword in normalized_goal for keyword in calculation_keywords):

        print("[PLANNER] Calculation task identified.")

        plan.append(
            PlanStep(
                step_id=len(plan) + 1,
                description="Calculate the requested result",
                tool_name="calculator"
            )
        )

    # General fallback
    if not plan:

        print("[PLANNER] General information task identified.")

        plan.append(
            PlanStep(
                step_id=1,
                description="Search for information related to the goal",
                tool_name="web_search"
            )
        )

        plan.append(
            PlanStep(
                step_id=2,
                description="Fetch a relevant information source",
                tool_name="fetch_url"
            )
        )

    print(
        f"[PLANNER] Generated {len(plan)} execution steps successfully."
    )

    for step in plan:
        print(
            f"[PLANNER] Step {step.step_id}: "
            f"{step.description} -> {step.tool_name}"
        )

    return plan
