
from urllib.parse import urlparse

from app.tools.web_search import web_search
from app.tools.fetch_url import fetch_url
from app.tools.calculator import calculate
from app.recovery.retry import retry_operation


class AgentExecutor:

    def __init__(self, demo_failure=False):
        self.search_results = []
        self.fetched_pages = []
        self.attempted_urls = set()
        self.tool_results = []
        self.failures = []
        self.recovery_events = []
        self.skipped_steps = []

        self.demo_failure = demo_failure
        self.demo_failure_triggered = False

    def execute_step(self, step, goal):

        print("\n" + "=" * 55)
        print(f"[EXECUTOR] STEP {step.step_id}")
        print(f"[EXECUTOR] Task: {step.description}")
        print(f"[EXECUTOR] Selected Tool: {step.tool_name}")
        print("=" * 55)

        if step.tool_name == "fetch_url" and not self.search_results:
            message = "Skipped: search results are unavailable."
            print(message)
            self.skipped_steps.append(step.step_id)

            self.failures.append({
                "step_id": step.step_id,
                "tool": step.tool_name,
                "error": message
            })

            return {"success": False, "error": message}

        if step.tool_name == "calculator" and not self.fetched_pages:
            message = "Skipped: no research pages were collected."
            print(message)
            self.skipped_steps.append(step.step_id)

            self.failures.append({
                "step_id": step.step_id,
                "tool": step.tool_name,
                "error": message
            })

            return {"success": False, "error": message}

        try:

            # TOOL 1: WEB SEARCH
            if step.tool_name == "web_search":

                queries = [
                    goal,
                    "Generative AI trends 2026",
                    "latest artificial intelligence developments 2026"
                ]

                for attempt, query in enumerate(queries, start=1):

                    print(f"[RECOVERY] Search attempt {attempt}")

                    result = web_search(query, max_results=5)

                    if result["success"] and result["results"]:
                        self.search_results = result["results"]
                        break

                if not self.search_results:
                    raise RuntimeError("All search attempts failed.")

                result = {
                    "success": True,
                    "results": self.search_results
                }

            # TOOL 2: URL FETCHER
            elif step.tool_name == "fetch_url":

                result = None

                for item in self.search_results:

                    url = item.get("url", "")

                    if not url or url in self.attempted_urls:
                        continue

                    parsed_url = urlparse(url)

                    if parsed_url.scheme not in ("http", "https"):
                        self.attempted_urls.add(url)
                        print(f"[VALIDATION] Invalid URL skipped: {url}")
                        continue

                    domain = parsed_url.netloc.lower()

                    blocked_domains = [
                        "bing.com",
                        "doubleclick.net",
                        "googleadservices.com",
                        "googlesyndication.com"
                    ]

                    if any(
                        domain == blocked or domain.endswith("." + blocked)
                        for blocked in blocked_domains
                    ):
                        self.attempted_urls.add(url)
                        print(f"[VALIDATION] Redirect URL skipped: {domain}")
                        continue

                    self.attempted_urls.add(url)

                    print(f"\n[EXECUTOR] Processing source: {url}")

                    def fetch_operation():

                        if (
                            self.demo_failure
                            and not self.demo_failure_triggered
                        ):
                            self.demo_failure_triggered = True

                            raise ConnectionError(
                                "Synthetic failure: simulated temporary timeout."
                            )

                        return fetch_url(url)

                    recovery = retry_operation(
                        operation=fetch_operation,
                        max_attempts=2,
                        delay=1,
                        operation_name="Website Fetch"
                    )

                    # Record retry history
                    if recovery["attempt_errors"]:

                        event = {
                            "step_id": step.step_id,
                            "tool": "fetch_url",
                            "url": url,
                            "attempts": recovery["attempts"],
                            "errors": recovery["attempt_errors"],
                            "recovered": recovery["success"]
                        }

                        self.recovery_events.append(event)

                        if recovery["success"]:
                            print(
                                "[EXECUTOR] Failure successfully recovered."
                            )

                    if recovery["success"]:

                        page = recovery["data"]

                        if (
                            isinstance(page, dict)
                            and page.get("success")
                            and page.get("content", "").strip()
                        ):
                            self.fetched_pages.append(page)
                            result = page
                            break

                        error_message = (
                            page.get("error", "No readable page content.")
                            if isinstance(page, dict)
                            else "Invalid fetch response."
                        )

                    else:
                        error_message = recovery["error"]

                    self.failures.append({
                        "step_id": step.step_id,
                        "tool": "fetch_url",
                        "url": url,
                        "error": error_message
                    })

                    print("[RECOVERY] Moving to another source.")

                if result is None:
                    raise RuntimeError(
                        "Unable to fetch any remaining valid source."
                    )

            # TOOL 3: CALCULATOR
            elif step.tool_name == "calculator":

                total = len(self.search_results)
                fetched = len(self.fetched_pages)

                if total == 0:
                    raise RuntimeError("No search results available.")

                expression = f"({fetched} / {total}) * 100"

                result = calculate(expression)

                if not result["success"]:
                    raise RuntimeError(result["error"])

            else:
                raise ValueError(f"Unknown tool: {step.tool_name}")

            self.tool_results.append({
                "step_id": step.step_id,
                "tool": step.tool_name,
                "success": True,
                "data": result
            })

            print("[EXECUTOR] Step completed successfully.")

            return {"success": True, "data": result}

        except Exception as error:

            print(f"[EXECUTOR] Step failed: {error}")

            self.failures.append({
                "step_id": step.step_id,
                "tool": step.tool_name,
                "error": str(error)
            })

            return {"success": False, "error": str(error)}

    def get_summary(self):

        # Count failures recovered through retry
        recovered_by_retry = sum(
            1 for event in self.recovery_events
            if event["recovered"]
        )

        # Count URLs that failed even after retries
        failed_source_urls = sum(
            1 for event in self.recovery_events
            if not event["recovered"]
        )

        # Count individual failed attempts
        failed_attempts = sum(
            len(event.get("errors", []))
            for event in self.recovery_events
        )

        # Identify fetch steps that had a source failure
        failed_fetch_steps = {
            item["step_id"]
            for item in self.failures
            if item["tool"] == "fetch_url" and item.get("url")
        }

        # Identify fetch steps that eventually fetched a page
        successful_fetch_steps = {
            item["step_id"]
            for item in self.tool_results
            if item["tool"] == "fetch_url"
        }

        # Count workflow steps that recovered using another source
        alternative_source_recoveries = len(
            failed_fetch_steps & successful_fetch_steps
        )

        # Identify steps that never completed successfully
        successful_steps = {
            item["step_id"]
            for item in self.tool_results
        }

        failed_steps = {
            item["step_id"]
            for item in self.failures
        }

        unresolved_workflow_steps = len(
            failed_steps - successful_steps
        )

        return {
            "total_search_results": len(self.search_results),

            "successfully_fetched_pages": len(self.fetched_pages),

            "successful_tool_executions": len(self.tool_results),

            "failed_source_urls": failed_source_urls,

            "failed_attempts": failed_attempts,

            "recovered_by_retry": recovered_by_retry,

            "alternative_source_recoveries": alternative_source_recoveries,

            "unresolved_workflow_steps": unresolved_workflow_steps,

            "recovery_events": self.recovery_events,

            "skipped_steps": self.skipped_steps,

            "sources": [
                {
                    "title": page.get("title", ""),
                    "url": page.get("url", "")
                }
                for page in self.fetched_pages
            ]
        }
