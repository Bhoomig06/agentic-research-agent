
from app.planner import create_plan


test_goals = [
    "Research the latest developments in Generative AI in 2026.",
    "Calculate the average score and percentage.",
    "Find information about AI agents."
]

for goal in test_goals:

    print("\n" + "=" * 60)
    print("USER GOAL:", goal)
    print("=" * 60)

    plan = create_plan(goal)

    print("\nGENERATED PLAN:")

    for step in plan:
        print(
            f"{step.step_id}. {step.description} "
            f"-> {step.tool_name}"
        )
