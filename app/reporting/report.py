
import json
from pathlib import Path
from datetime import datetime

from app.executor import AgentExecutor


def generate_reports(goal, plan, executor, output_dir="reports"):

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    summary = executor.get_summary()

    # Extract collected research sources
    research_sources = []

    for page in executor.fetched_pages:

        content = page.get("content", "")

        research_sources.append({
            "title": page.get("title", ""),
            "url": page.get("url", ""),
            "content_excerpt": content[:1500]
        })

    # Determine execution status
    if summary["unresolved_workflow_steps"] > 0:
        execution_status = "incomplete"

    elif summary["failed_source_urls"] > 0:
        execution_status = "completed_with_warnings"

    else:
        execution_status = "completed"

    # Prepare structured JSON report
    report_data = {

        "project": "Agentic Research and Decision Agent",

        "generated_at": datetime.now().isoformat(),

        "goal": goal,

        "planner_type": "Rule-based local planner",

        "execution_status": execution_status,

        "execution_plan": [
            {
                "step_id": step.step_id,
                "description": step.description,
                "tool": step.tool_name
            }
            for step in plan
        ],

        "execution_summary": summary,

        "research_sources": research_sources,

        "tool_execution_history": executor.tool_results,

        "recovery_history": executor.recovery_events,

        "unresolved_failures": executor.failures
    }

    # Generate JSON report
    json_file = output_path / "research_report.json"

    with open(json_file, "w", encoding="utf-8") as file:

        json.dump(
            report_data,
            file,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    # Generate Markdown report
    markdown = []

    markdown.append("# Agentic Research Report")
    markdown.append("")

    markdown.append(
        f"**Generated:** {report_data['generated_at']}"
    )

    markdown.append("")

    markdown.append("## 1. Research Goal")
    markdown.append(goal)
    markdown.append("")

    markdown.append("## 2. Execution Status")
    markdown.append(execution_status.upper())
    markdown.append("")

    markdown.append("## 3. Execution Plan")

    for step in plan:

        markdown.append(
            f"- Step {step.step_id}: {step.description} "
            f"(Tool: {step.tool_name})"
        )

    markdown.append("")

    markdown.append("## 4. Execution Summary")

    markdown.append(
        f"- Total search results: {summary['total_search_results']}"
    )

    markdown.append(
        f"- Successfully fetched pages: "
        f"{summary['successfully_fetched_pages']}"
    )

    markdown.append(
        f"- Successful tool executions: "
        f"{summary['successful_tool_executions']}"
    )

    markdown.append(
        f"- Failed source URLs: {summary['failed_source_urls']}"
    )

    markdown.append(
        f"- Failed attempts: {summary['failed_attempts']}"
    )

    markdown.append(
        f"- Recovered by retry: {summary['recovered_by_retry']}"
    )

    markdown.append(
        f"- Alternative-source recoveries: "
        f"{summary['alternative_source_recoveries']}"
    )

    markdown.append(
        f"- Unresolved workflow steps: "
        f"{summary['unresolved_workflow_steps']}"
    )

    markdown.append("")

    markdown.append("## 5. Research Sources")

    if research_sources:

        for index, source in enumerate(research_sources, start=1):

            markdown.append(
                f"### {index}. {source['title']}"
            )

            markdown.append(
                f"Source: {source['url']}"
            )

            markdown.append("")

            markdown.append(
                source["content_excerpt"]
            )

            markdown.append("")

    else:

        markdown.append(
            "No research sources were successfully collected."
        )

    markdown.append("")

    markdown.append("## 6. Recovery History")

    if executor.recovery_events:

        for event in executor.recovery_events:

            markdown.append(
                f"### Source: {event.get('url', 'Unknown')}"
            )

            markdown.append(
                f"- Attempts: {event.get('attempts', 0)}"
            )

            markdown.append(
                f"- Recovered by retry: "
                f"{event.get('recovered', False)}"
            )

            for error in event.get("errors", []):

                markdown.append(
                    f"- Attempt {error['attempt']} error: "
                    f"{error['error']}"
                )

            markdown.append("")

    else:

        markdown.append("No retry events recorded.")

    markdown.append("")

    markdown.append("## 7. Limitations")

    markdown.append(
        "- The planner currently uses predefined rules "
        "rather than an LLM."
    )

    markdown.append(
        "- Research quality depends on external search results "
        "and website availability."
    )

    markdown.append(
        "- Extracted webpage content is presented as source material "
        "and is not independently verified."
    )

    markdown.append(
        "- The calculator measures the percentage of search results "
        "successfully fetched, not research quality."
    )

    markdown.append(
        "- The current agent does not generate a fully verified "
        "synthesis or ranking of research findings."
    )

    markdown.append("")

    markdown.append("## 8. Conclusion")

    if execution_status == "completed":

        markdown.append(
            "The agent completed its research workflow successfully."
        )

    elif execution_status == "completed_with_warnings":

        markdown.append(
            "The agent completed its research workflow with some "
            "source-access failures. It continued using alternative "
            "sources and collected research information."
        )

    else:

        markdown.append(
            "The agent could not complete all planned workflow steps."
        )

    markdown.append("")

    markdown.append(
        "The execution demonstrates multi-tool usage, "
        "failure logging, retry handling, and alternative-source recovery."
    )

    markdown_file = output_path / "research_report.md"

    with open(markdown_file, "w", encoding="utf-8") as file:

        file.write("\n".join(markdown))

    print("\n[REPORTING] Reports generated successfully.")

    print(f"[REPORTING] JSON: {json_file}")

    print(f"[REPORTING] Markdown: {markdown_file}")

    return {
        "json_report": str(json_file),
        "markdown_report": str(markdown_file)
    }
