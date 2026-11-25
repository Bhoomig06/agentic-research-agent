
from ddgs import DDGS


def web_search(query: str, max_results: int = 5) -> dict:
    """
    Search the web and return relevant results.
    """

    print(f"\n[WEB SEARCH] Searching for: {query}")

    try:
        results = DDGS().text(
            query,
            max_results=max_results
        )

        search_results = []

        for item in results:
            search_results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", "")
            })

        if not search_results:
            return {
                "success": False,
                "results": [],
                "error": "No search results found."
            }

        print(f"[WEB SEARCH] Found {len(search_results)} results.")

        return {
            "success": True,
            "results": search_results,
            "error": None
        }

    except Exception as error:
        print(f"[WEB SEARCH ERROR] {error}")

        return {
            "success": False,
            "results": [],
            "error": str(error)
        }
