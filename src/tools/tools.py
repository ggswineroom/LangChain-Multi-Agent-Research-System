
import os

import requests
import trafilatura  # noqa: F401

## for scraping web pages
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from readability import Document  # noqa: F401
from rich import print
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool (description= "Search the web for the information matching the user's query")
def web_search(query: str) -> str:
    """
    Search the web using Tavily and return the top results.
    """
    results = tavily.search(query=query, limit=5)
    
    print(results)
    
    out = []  # empty list to store formatted results
    
    for r in results['results']:
        out.append(
            f"Title:{r['title']}\nURL: {r['url']}\nSnippet:{r ['content'][:300]}\n"
            )
        
    return "\n".join(out)   
   
    
    
@tool(description="Scrap the text for the url provided")
def scrape_url(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove elements that aren't useful as page content
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside"
    ]):
        element.decompose()

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    return text