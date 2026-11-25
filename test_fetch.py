
from app.tools.fetch_url import fetch_url

url = "https://www.techtarget.com/ai/feature/The-future-of-generative-AI-10-trends-to-follow-in-2026"

result = fetch_url(url)

print("\nFETCH RESULT\n")

if result["success"]:
    print("Title:", result["title"])
    print("URL:", result["url"])
    print("\nExtracted Content:\n")
    print(result["content"][:2000])
else:
    print("Error:", result["error"])
