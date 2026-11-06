import urllib.parse
import requests


USER_AGENT = "MiniResearcher/1.0 (academic research assistant; contact: info@example.com)"


def search_wikipedia(query: str) -> str:
    """Search Wikipedia and return a factual summary, title, and page URL.

    Args:
        query: The search term, topic, or person to look up.

    Returns:
        A formatted string with the title, canonical URL, and summary extract.
    """
    headers = {"User-Agent": USER_AGENT}

    try:
        # Step 1: Search Wikipedia for matching page titles
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 3,
        }
        res = requests.get(search_url, params=search_params, headers=headers, timeout=10)
        res.raise_for_status()
        search_data = res.json()

        results = search_data.get("query", {}).get("search", [])
        if not results:
            return f"No Wikipedia articles found for '{query}'."

        best_title = results[0]["title"]

        # Step 2: Fetch article summary from Wikipedia REST API
        encoded_title = urllib.parse.quote(best_title.replace(" ", "_"))
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
        summary_res = requests.get(summary_url, headers=headers, timeout=10)

        if summary_res.status_code == 200:
            data = summary_res.json()
            title = data.get("title", best_title)
            extract = data.get("extract", "No summary available.")
            page_url = data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{encoded_title}")
            return f"Title: {title}\nURL: {page_url}\n\nSummary:\n{extract}"

        return f"Found article '{best_title}' on Wikipedia, but could not load the summary."

    except Exception as e:
        return f"Wikipedia search error: {str(e)}"
