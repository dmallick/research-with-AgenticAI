# URL text extraction logic

import requests
from bs4 import BeautifulSoup

def extract_url_content(url: str) -> str:
    """Scrapes and cleans visible text content from the target URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text(separator=' ')
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return " ".join(chunk for chunk in chunks if chunk)
        return f"Failed to retrieve content. Status code: {response.status_code}"
    except Exception as e:
        return f"Error scraping URL: {str(e)}"