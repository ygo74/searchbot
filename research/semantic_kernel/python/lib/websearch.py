import os
import requests
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# pip install newspaper3k
from newspaper import Article

def google_search(query: str, num_results: int = 2, max_chars: int = 500) -> list:
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_CENTER_CONNECTION_ID")

    if not api_key or not search_engine_id:
        raise ValueError("API key or Search Engine ID not found in environment variables")

    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": search_engine_id, "q": query, "num": num_results}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(response.json())
        raise Exception(f"Error in API request: {response.status_code}")

    results = response.json().get("items", [])

    def get_page_content(url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            text = ' '.join(soup.stripped_strings)
            if max_chars == 0:
                return text

            return text[:max_chars].rsplit(' ', 1)[0]
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return ""

    enriched_results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(get_page_content, item["link"]): item for item in results}
        for future in as_completed(future_to_url):
            item = future_to_url[future]
            body = future.result()
            enriched_results.append(
                {"title": item["title"], "link": item["link"], "snippet": item["snippet"], "body": body}
            )

    return enriched_results

def google_search_with_article(query: str, num_results: int = 2, max_chars: int = 500) -> list:
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_CENTER_CONNECTION_ID")

    if not api_key or not search_engine_id:
        raise ValueError("API key or Search Engine ID not found in environment variables")

    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": search_engine_id, "q": query, "num": num_results}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(response.json())
        raise Exception(f"Error in API request: {response.status_code}")

    results = response.json().get("items", [])

    def get_page_content(url: str) -> str:
        try:
            article = Article(url)
            article.download()
            article.parse()
            content = article.text
            if len(content) > max_chars:
                content = content[:max_chars].rsplit(' ', 1)[0]
            return content
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return ""

    enriched_results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(get_page_content, item["link"]): item for item in results}
        for future in as_completed(future_to_url):
            item = future_to_url[future]
            body = future.result()
            enriched_results.append(
                {"title": item["title"], "link": item["link"], "snippet": item["snippet"], "body": body}
            )

    return enriched_results