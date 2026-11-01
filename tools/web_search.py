import os
from googleapiclient.discovery import build


def web_search(query, num_results=5):
    """Search the web using Google Custom Search API.

    Args:
        query: The search query string.
        num_results: Number of results to return (max 10).

    Returns:
        A formatted string containing the search results with
        title, link, and snippet for each result.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")

    if not api_key or not cse_id:
        return (
            "Error: GOOGLE_API_KEY and GOOGLE_CSE_ID must be set "
            "in the .env file."
        )

    try:
        service = build("customsearch", "v1", developerKey=api_key)

        result = (
            service.cse()
            .list(q=query, cx=cse_id, num=min(num_results, 10))
            .execute()
        )

        if "items" not in result:
            return f"No results found for: {query}"

        search_results = []

        for i, item in enumerate(result["items"], 1):
            title = item.get("title", "No title")
            link = item.get("link", "No link")
            snippet = item.get("snippet", "No description")

            search_results.append(
                f"{i}. {title}\n"
                f"   URL: {link}\n"
                f"   {snippet}"
            )

        return "\n\n".join(search_results)

    except Exception as e:
        return f"Search error: {str(e)}"
