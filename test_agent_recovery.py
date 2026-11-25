
from app.planner import create_plan
from app.executor import AgentExecutor


goal = "Research the latest developments in Generative AI in 2026."

print("\nSTARTING INTEGRATED AGENT RECOVERY TEST")

plan = create_plan(goal)

# Enable one controlled synthetic failure
executor = AgentExecutor(demo_failure=True)

for step in plan:

    result = executor.execute_step(step, goal)

    if not result["success"]:
        print(f"[MAIN] Step {step.step_id} could not complete.")

print("\nFINAL EXECUTION SUMMARY")

print(executor.get_summary())
