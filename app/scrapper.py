import requests
from bs4 import BeautifulSoup

def scrape_jooble():
    jobs = []
    
    url = "https://es.jooble.org/SearchResult?rgns=España&ukw=data%20freelance"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    for item in soup.select(".result"):
        text = item.get_text(strip=True)

        jobs.append({
            "title": text,
            "company": "N/A",
            "description": text,
            "source": "Jooble",
            "url": ""
        })

    return jobs
