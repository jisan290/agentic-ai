import re
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36 MiniResearcher/1.0"
    )
}


def scrape_webpage(url: str, max_chars: int = 4000) -> str:
    """Fetch and extract readable plain text content from a web page URL.

    Args:
        url: The web URL to fetch and parse.
        max_chars: Maximum characters of text to return (default: 4000).

    Returns:
        The extracted page title and readable content.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, headers=HEADERS, timeout=12)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unneeded elements
        for element in soup(["script", "style", "nav", "footer", "header", "noscript", "svg", "form"]):
            element.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

        # Prefer main content containers if present
        content_container = soup.find("article") or soup.find("main") or soup.body
        if not content_container:
            return f"Title: {title}\nURL: {url}\n\nCould not extract readable body content."

        # Extract text paragraphs and headers
        lines = []
        for tag in content_container.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            text = tag.get_text(separator=" ", strip=True)
            if text and len(text) > 20:
                lines.append(text)

        extracted_text = "\n\n".join(lines)
        if not extracted_text:
            extracted_text = content_container.get_text(separator="\n", strip=True)

        # Collapse excessive whitespace
        extracted_text = re.sub(r"\n{3,}", "\n\n", extracted_text)

        if len(extracted_text) > max_chars:
            extracted_text = extracted_text[:max_chars] + f"\n\n... [Truncated after {max_chars} characters]"

        return f"Title: {title}\nURL: {url}\n\nContent:\n{extracted_text}"

    except requests.exceptions.RequestException as e:
        return f"Failed to fetch {url}: {str(e)}"
    except Exception as e:
        return f"Web scraper error: {str(e)}"
