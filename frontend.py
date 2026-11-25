import json
import io
from pathlib import Path
from contextlib import redirect_stdout

import streamlit as st

from app.planner import create_plan
from app.executor import AgentExecutor
from app.reporting.report import generate_reports


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Agentic Research Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic Research & Decision Agent")
st.caption(
    "An automated research assistant that plans tasks, "
    "uses tools, handles failures, and generates reports."
)

st.divider()


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("About the Agent")
    st.write(
        "This agent uses a local rule-based planner, "
        "web search, webpage extraction, and recovery logic."
    )

    st.subheader("Available Tools")
    st.write("🔎 Web Search")
    st.write("🌐 URL Fetcher")
    st.write("🧮 Calculator")

    st.divider()

    demo_failure = st.checkbox(
        "Enable synthetic failure demo",
        value=False,
        help="Simulates a temporary timeout to demonstrate recovery."
    )

    st.caption("Built with Python and Streamlit")


# ---------------- USER INPUT ----------------

st.subheader("1. Enter Your Research Goal")

goal = st.text_area(
    "What would you like the agent to research?",
    value="Research the latest developments in Generative AI in 2026.",
    height=100,
    placeholder="Enter a research goal..."
)

run_button = st.button(
    "🚀 Run Research Agent",
    type="primary",
    use_container_width=True
)


# ---------------- EXECUTION ----------------

if run_button:

    if not goal.strip():
        st.warning("Please enter a research goal.")

    else:
        output_buffer = io.StringIO()

        try:
            with redirect_stdout(output_buffer):

                # Step 1: Planning
                plan = create_plan(goal.strip())

                # Step 2: Initialize executor
                executor = AgentExecutor(
                    demo_failure=demo_failure
                )

                # Step 3: Execute planned steps
                for step in plan:
                    executor.execute_step(step, goal.strip())

                # Step 4: Generate reports
                report_files = generate_reports(
                    goal.strip(),
                    plan,
                    executor
                )

                # Step 5: Collect results
                summary = executor.get_summary()

            st.session_state["agent_run"] = {
                "goal": goal.strip(),
                "plan": plan,
                "executor": executor,
                "summary": summary,
                "report_files": report_files,
                "logs": output_buffer.getvalue(),
                "error": None
            }

        except Exception as error:
            st.session_state["agent_run"] = {
                "goal": goal.strip(),
                "logs": output_buffer.getvalue(),
                "error": str(error)
            }


# ---------------- DISPLAY RESULTS ----------------

if "agent_run" in st.session_state:

    run_data = st.session_state["agent_run"]

    st.divider()
    st.subheader("2. Agent Execution Results")

    if run_data["error"]:

        st.error(
            f"An error occurred while running the agent: "
            f"{run_data['error']}"
        )

        with st.expander("Execution logs"):
            st.code(run_data["logs"], language="text")

    else:

        plan = run_data["plan"]
        executor = run_data["executor"]
        summary = run_data["summary"]
        report_files = run_data["report_files"]

        # Execution plan
        st.markdown("### 📋 Execution Plan")

        for step in plan:
            st.write(
                f"**Step {step.step_id}:** "
                f"{step.description} "
                f"— Tool: `{step.tool_name}`"
            )

        # Summary metrics
        st.markdown("### 📊 Execution Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Search Results",
            summary["total_search_results"]
        )

        col2.metric(
            "Pages Fetched",
            summary["successfully_fetched_pages"]
        )

        col3.metric(
            "Failed Attempts",
            summary["failed_attempts"]
        )

        col4.metric(
            "Unresolved Steps",
            summary["unresolved_workflow_steps"]
        )

        status = (
            "Incomplete"
            if summary["unresolved_workflow_steps"] > 0
            else (
                "Completed with warnings"
                if summary["failed_source_urls"] > 0
                else "Completed"
            )
        )

        if status == "Completed":
            st.success(f"Execution Status: {status}")
        elif status == "Incomplete":
            st.error(f"Execution Status: {status}")
        else:
            st.warning(f"Execution Status: {status}")

        # Tool execution history
        st.divider()
        st.markdown("### 🛠️ Tool Execution History")

        if executor.tool_results:
            for item in executor.tool_results:
                with st.expander(
                    f"Step {item['step_id']} — {item['tool']}"
                ):
                    st.write("Status: Successful")
                    st.json(item["data"])
        else:
            st.info("No successful tool executions recorded.")

        # Recovery history
        st.divider()
        st.markdown("### 🔄 Failure & Recovery History")

        recovery_events = summary["recovery_events"]

        if recovery_events:
            for event in recovery_events:
                with st.expander(
                    f"Recovery event — {event.get('tool', 'Tool')}"
                ):
                    st.write("URL:", event.get("url", "Unknown"))
                    st.write("Attempts:", event.get("attempts", 0))
                    st.write(
                        "Recovered by retry:",
                        event.get("recovered", False)
                    )
                    st.json(event.get("errors", []))
        else:
            st.info("No retry events recorded in this run.")

        st.write(
            "Alternative-source recoveries:",
            summary["alternative_source_recoveries"]
        )

        st.write(
            "Failed source URLs:",
            summary["failed_source_urls"]
        )

        # Sources
        st.divider()
        st.markdown("### 🌐 Research Sources")

        if executor.fetched_pages:
            for index, page in enumerate(
                executor.fetched_pages,
                start=1
            ):
                with st.expander(
                    f"{index}. {page.get('title', 'Untitled source')}"
                ):
                    st.write(page.get("url", ""))
                    st.write(
                        page.get("content", "")[:1500]
                    )
        else:
            st.info("No webpage content was successfully collected.")

        # Full execution logs
        st.divider()
        st.markdown("### 📝 Execution Logs")

        with st.expander("View detailed agent logs"):
            st.code(run_data["logs"], language="text")

        # Reports
        st.divider()
        st.markdown("### 📁 Generated Reports")

        json_path = Path(report_files["json_report"])
        markdown_path = Path(report_files["markdown_report"])

        col1, col2 = st.columns(2)

        if json_path.exists():
            with col1:
                st.download_button(
                    label="⬇️ Download JSON Report",
                    data=json_path.read_bytes(),
                    file_name="research_report.json",
                    mime="application/json",
                    use_container_width=True
                )

        if markdown_path.exists():
            with col2:
                st.download_button(
                    label="⬇️ Download Markdown Report",
                    data=markdown_path.read_bytes(),
                    file_name="research_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

        if json_path.exists():
            with st.expander("Preview JSON Report"):
                report_data = json.loads(
                    json_path.read_text(encoding="utf-8")
                )
                st.json(report_data)

        st.caption(
            "Note: The planner is rule-based. Extracted webpage "
            "content is source material and is not independently verified."
        )
