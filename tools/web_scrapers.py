# URL text extraction logic

import requests
from bs4 import BeautifulSoup

def extract_url_content(url: str) -> str:
    """Scrapes and cleans visible text content from the target URL using optimized browser headers."""
    try:
        # A complete header set makes the request look like standard desktop browser traffic
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Stripping scripts, styling and tracking elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.extract()
                
            text = soup.get_text(separator=' ')
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return " ".join(chunk for chunk in chunks if chunk)
            
        return f"Failed to retrieve content. Status code: {response.status_code}"
    except Exception as e:
        return f"Error scraping URL: {str(e)}"