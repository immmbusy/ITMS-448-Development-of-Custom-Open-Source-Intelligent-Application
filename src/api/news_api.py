import requests

NEWS_API_KEY = "your_newsapi_key"

def fetch_news_data(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("status") != "ok":
        raise Exception("Failed to fetch news!")
    
    return data.get("articles", [])[:5]  # Return top 5 articles
