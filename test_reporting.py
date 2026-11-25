
from app.planner import create_plan
from app.executor import AgentExecutor
from app.reporting.report import generate_reports


goal = "Research the latest developments in Generative AI in 2026."

print("\nSTARTING RESEARCH AGENT")

plan = create_plan(goal)

executor = AgentExecutor(demo_failure=True)

for step in plan:
    result = executor.execute_step(step, goal)

    if not result["success"]:
        print(
            f"[MAIN] Step {step.step_id} failed: "
            f"{result['error']}"
        )

print("\nGENERATING FINAL REPORT")

files = generate_reports(
    goal=goal,
    plan=plan,
    executor=executor
)

print("\nGENERATED FILES")
print(files)

print("\nFINAL SUMMARY")
print(executor.get_summary())
