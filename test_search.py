
from app.tools.web_search import web_search

query = "Latest developments in Generative AI 2026"

response = web_search(query, max_results=5)

print("\nSEARCH RESULTS\n")

if response["success"]:
    for index, result in enumerate(response["results"], start=1):
        print(f"\n{index}. {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Summary: {result['snippet']}")
else:
    print("Search failed:", response["error"])
