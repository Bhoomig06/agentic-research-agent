# Agentic Research and Decision Agent

## Design and Implementation Write-up

### 1. Problem Statement and Domain

The project focuses on automated web research. Its objective is to accept a high-level user goal, break it into smaller execution steps, use multiple tools to collect information, handle failures, and generate structured reports.

### 2. System Design

The system follows a modular architecture with five main stages:

- **Planning:** A keyword-based planner identifies the task category and generates an execution plan.
- **Execution:** The executor coordinates the selected tools and manages the workflow.
- **Tool Usage:** Web Search discovers relevant sources, URL Fetcher extracts webpage content, and Calculator performs safe mathematical operations.
- **Failure Recovery:** A retry mechanism handles temporary failures. If a source remains unavailable, the executor attempts another available source.
- **Reporting:** The reporting module generates JSON and Markdown reports containing execution details, collected sources, failures, and recovery history.

### 3. Design Decisions

A local rule-based planner was selected to keep the prototype lightweight and independent of paid LLM APIs. Python modules were separated by responsibility to improve maintainability.

The calculator uses Python AST parsing with an allowlist of supported mathematical operations instead of unrestricted `eval()`. Synthetic failures were introduced to test the recovery mechanism under controlled conditions.

### 4. Assumptions and Test Data

- The user provides a clear research goal.
- Internet connectivity is available for web search and webpage fetching.
- Search results may contain unavailable, invalid, or redirected URLs.
- Synthetic network failures are used for repeatable recovery testing.
- Collected webpage content is treated as source material and is not independently verified.

### 5. Testing and Results

Three sample execution logs demonstrate the system's functionality:

1. **Integrated research workflow:** The agent searches the web, fetches two sources, records a simulated failure, and switches to an alternative source.
2. **Retry mechanism:** A simulated network timeout occurs on the first attempt, and the operation succeeds on the second attempt.
3. **Calculator tool:** Three mathematical expressions are evaluated successfully, covering multiplication, average calculation, and subtraction.

The integrated research test completed all planned workflow steps with zero unresolved workflow failures. The execution also recorded one failed source and one alternative-source recovery.

### 6. Limitations

- The planner currently uses keyword-based rules rather than LLM-based reasoning.
- The system does not yet generate a fully verified synthesis of research findings.
- Website availability and extracted content depend on external sources.
- Natural-language mathematical expressions are not automatically converted into calculator expressions.
- The current prototype does not maintain persistent memory across separate runs.

### 7. Future Improvements

- Integrate an LLM for more flexible planning and decision-making.
- Add dynamic tool selection based on task requirements.
- Generate research summaries with source references.
- Improve source validation and automated testing.
- Add persistent memory for multi-step tasks.
- Introduce more tools and structured evaluation metrics.

### 8. Development Details

- **Domain:** Automated Web Research and Decision Support
- **Implementation Language:** Python
- **Tools:** DuckDuckGo Search, Requests, BeautifulSoup, Python AST, JSON
- **Testing:** Synthetic failure scenarios and live web requests
- **Development Time:** [Approximately 18 hours]

