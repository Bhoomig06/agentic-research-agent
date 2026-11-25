# Agentic Research and Decision Agent

A lightweight agentic system that accepts natural-language goals, creates goal-aware execution plans, uses multiple tools, handles failures, and generates structured research reports.

## Project Overview

The Agentic Research and Decision Agent automates a research workflow using a local rule-based planner and multiple tools.

It can:
- Accept a high-level natural-language goal.
- Generate an execution plan based on goal keywords.
- Search the web for relevant information.
- Fetch and extract webpage content.
- Perform safe mathematical calculations.
- Retry failed operations.
- Switch to alternative sources when a website is unavailable.
- Generate JSON and Markdown reports.
- Maintain visible execution logs.

## Architecture

The system consists of:
1. Planner – creates goal-aware execution plans.
2. Executor – coordinates planned tasks.
3. Web Search Tool – discovers relevant sources.
4. URL Fetcher – extracts webpage content.
5. Calculator – evaluates mathematical expressions safely.
6. Recovery Manager – retries failed requests and selects alternative sources.
7. Report Generator – creates structured reports.

See `docs/architecture.md` for the architecture diagram.

## Technology Stack

- Python 3
- DuckDuckGo Search (`ddgs`)
- Requests
- BeautifulSoup
- Python AST
- JSON
- Markdown

## Project Structure

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
│   └── architecture.md
├── reports/
│   ├── research_report.json
│   └── research_report.md
├── logs/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd agentic-research-agent
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

Run the reporting demonstration:

```bash
python test_reporting.py
```

Run planner tests:

```bash
python test_planner.py
```

Run the integrated failure-recovery demonstration:

```bash
python test_agent_recovery.py
```

Generated reports are saved in the `reports/` directory.

## Example Goal

```text
Research the latest developments in Generative AI in 2026.
```

The planner generates research steps, the executor searches and fetches webpages, and the reporting module produces JSON and Markdown outputs.

## Failure Recovery Demonstration

The project includes a synthetic temporary network failure.

The recovery mechanism:
1. Attempts the requested operation.
2. Records the failure.
3. Retries the operation.
4. Moves to another source if the URL remains unavailable.
5. Records recovery events and unresolved failures.

## Testing

The project includes tests for:
- Planning
- Web search
- URL fetching
- Calculator
- Executor
- Retry mechanism
- Integrated failure recovery
- Report generation

## Design Decisions

The planner uses local keyword-based rules instead of an external LLM API. This keeps the prototype lightweight and avoids API costs.

The calculator uses Python AST parsing with an allowlist of mathematical operations rather than unrestricted `eval()`.

The recovery manager records individual failures and supports retry and alternative-source selection.

## Limitations

- Planning is keyword-based rather than LLM-driven.
- Search results and website access depend on external services.
- Webpage extraction may be incomplete.
- The system does not yet generate a verified synthesis of research findings.
- The calculator currently evaluates expressions provided by the executor rather than extracting arbitrary expressions from natural-language goals.

## Future Improvements

- Integrate an LLM-based planning module.
- Add dynamic tool selection.
- Generate research summaries with source references.
- Add more tools and APIs.
- Introduce persistent execution memory.
- Add automated tests and evaluation metrics.

## Author

Bhoomi Garg

B.Tech Computer Science and Engineering
