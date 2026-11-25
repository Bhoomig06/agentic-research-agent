
from app.planner import create_plan
from app.executor import AgentExecutor

goal = "Research the latest developments in Generative AI in 2026."

print("\nSTARTING AGENT EXECUTION")

plan = create_plan(goal)

print("\nGENERATED PLAN")

for step in plan:
    print(f"{step.step_id}. {step.description} ({step.tool_name})")

executor = AgentExecutor()

for step in plan:
    result = executor.execute_step(step, goal)

    if not result["success"]:
        print("Step needs recovery:", result["error"])

print("\nEXECUTION SUMMARY")
print("Search results:", len(executor.search_results))
print("Fetched pages:", len(executor.fetched_pages))
print("Successful tool executions:", len(executor.tool_results))
print("Failures:", len(executor.failures))
