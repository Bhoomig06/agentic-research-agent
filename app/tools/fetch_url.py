
import requests
from bs4 import BeautifulSoup


def fetch_url(url: str) -> dict:
    """
    Fetch webpage content and extract readable text.
    """

    print(f"\n[URL FETCHER] Opening: {url}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; ResearchAgent/1.0)"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary webpage elements
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript"
        ]):
            element.decompose()

        title = soup.title.get_text(strip=True) if soup.title else ""

        content = soup.get_text(separator=" ", strip=True)

        # Keep the extracted content manageable
        content = content[:8000]

        if not content:
            return {
                "success": False,
                "url": url,
                "title": title,
                "content": "",
                "error": "No readable content found."
            }

        print("[URL FETCHER] Content extracted successfully.")

        return {
            "success": True,
            "url": url,
            "title": title,
            "content": content,
            "error": None
        }

    except requests.Timeout:
        return {
            "success": False,
            "url": url,
            "title": "",
            "content": "",
            "error": "Request timed out."
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "url": url,
            "title": "",
            "content": "",
            "error": str(error)
        }
