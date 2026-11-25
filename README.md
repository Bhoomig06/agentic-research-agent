# Agentic Research and Decision Agent

A lightweight agentic system that accepts natural-language goals, creates goal-aware execution plans, uses multiple tools, handles failures, and generates structured research reports.

## 1. Project Overview

The Agentic Research and Decision Agent automates a research workflow using a local rule-based planner and multiple tools.

### Key Features

- Accepts high-level natural-language goals.
- Generates execution plans based on goal keywords.
- Searches the web for relevant information.
- Fetches and extracts webpage content.
- Performs safe mathematical calculations.
- Retries failed operations.
- Switches to alternative sources when a webpage is unavailable.
- Records execution and recovery events.
- Generates JSON and Markdown reports.
- Provides a Streamlit dashboard for interacting with the agent.

## 2. Architecture

The system consists of the following components:

1. **Planner:** Creates goal-aware execution plans.
2. **Executor:** Coordinates planned tasks and tool execution.
3. **Web Search Tool:** Discovers relevant sources.
4. **URL Fetcher:** Extracts webpage content.
5. **Calculator:** Evaluates mathematical expressions safely.
6. **Recovery Manager:** Retries failed requests and selects alternative sources.
7. **Report Generator:** Creates structured reports.
8. **Streamlit Frontend:** Displays execution plans, tool results, recovery information, and downloadable reports.

See `docs/architecture.md` for the architecture diagram.

## 3. Technology Stack

- Python 3
- Streamlit
- DuckDuckGo Search (`ddgs`)
- Requests
- BeautifulSoup
- Python AST
- JSON
- Markdown

## 4. Project Structure

```text
agentic-research-agent/
├── app/
│   ├── tools/
│   │   ├── web_search.py
│   │   ├── fetch_url.py
│   │   └── calculator.py
│   ├── recovery/
│   │   └── retry.py
│   ├── reporting/
│   │   └── report.py
│   ├── models.py
│   ├── planner.py
│   └── executor.py
├── docs/
│   ├── architecture.md
│   └── design_writeup.md
├── logs/
│   ├── sample_run_1.txt
│   ├── sample_run_2.txt
│   └── sample_run_3.txt
├── reports/
│   ├── research_report.json
│   └── research_report.md
├── frontend.py
├── main.py
├── requirements.txt
├── README.md
├── test_planner.py
├── test_search.py
├── test_fetch.py
├── test_calculator.py
├── test_executor.py
├── test_recovery.py
├── test_reporting.py
└── test_agent_recovery.py
```

## 5. Installation

Clone the repository:

```bash
git clone https://github.com/Bhoomig06/agentic-research-agent.git
cd agentic-research-agent
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 6. Run the Project

### Launch the Streamlit Dashboard

```bash
python -m streamlit run frontend.py
```

The dashboard allows users to:
- Enter a research goal.
- View the generated execution plan.
- Inspect tool execution results.
- View failure and recovery information.
- Explore collected research sources.
- Download JSON and Markdown reports.
- Enable a synthetic failure demonstration.

### Run Backend Demonstrations

Integrated reporting demonstration:

```bash
python test_reporting.py
```

Planner tests:

```bash
python test_planner.py
```

Integrated failure-recovery demonstration:

```bash
python test_agent_recovery.py
```

Generated reports are saved in the `reports/` directory.

## 7. Example Goal

```text
Research the latest developments in Generative AI in 2026.
```

The planner generates research steps, the executor searches and fetches webpages, and the reporting module produces JSON and Markdown outputs.

## 8. Failure Recovery Demonstration

The project includes controlled synthetic network failures to test recovery behaviour.

The recovery mechanism:

1. Attempts the requested operation.
2. Records the failure.
3. Retries the operation.
4. Moves to another source if the URL remains unavailable.
5. Records recovery events and unresolved failures.

The Streamlit dashboard includes an option to enable the synthetic failure demonstration.

## 9. Testing

The project includes individual test scripts covering:

- Planning
- Web search
- URL fetching
- Calculator functionality
- Executor behaviour
- Retry mechanism
- Integrated failure recovery
- Report generation

Sample execution traces are available in the `logs/` directory.

| Log file | Demonstration |
|---|---|
| `sample_run_1.txt` | Synthetic failure and alternative-source recovery |
| `sample_run_2.txt` | Successful retry after a simulated timeout |
| `sample_run_3.txt` | Calculator functional tests |

## 10. Design Decisions

The planner uses local keyword-based rules instead of an external LLM API. This keeps the prototype lightweight and avoids API costs.

The calculator uses Python AST parsing with an allowlist of mathematical operations rather than unrestricted `eval()`.

The recovery manager records individual failures and supports retry and alternative-source selection.

## 11. Limitations

- Planning is keyword-based rather than LLM-driven.
- Search results and website access depend on external services.
- Webpage extraction may be incomplete.
- The system does not yet generate a verified synthesis of research findings.
- The calculator currently evaluates expressions provided by the executor rather than extracting arbitrary expressions from natural-language goals.
- Execution activity is displayed after completion rather than streamed live.

## 12. Future Improvements

- Integrate an LLM-based planning module.
- Add dynamic tool selection.
- Generate research summaries with source references.
- Add more tools and APIs.
- Introduce persistent execution memory.
- Add automated tests and evaluation metrics.
- Improve monitoring and execution visualisation.

## 13. Documentation

Additional project documentation:

- `docs/architecture.md` – System architecture and component workflow.
- `docs/design_writeup.md` – Design decisions, assumptions, testing, limitations, and future improvements.
- `logs/` – Sample execution traces.
- `reports/` – Generated research reports.

## Author

**Bhoomi Garg**

B.Tech Computer Science and Engineering