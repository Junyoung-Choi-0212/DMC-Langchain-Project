import requests

def search_serper_links(query, api_key, max_results = 5):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": max_results
    }

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    results = []
    for item in data.get("organic", []):
        link = item.get("link", "")
        if ".go.kr" in link:
            results.append(link)

    return results