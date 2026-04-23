import os
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Ajusta esto a tu fuente real
BASE_URL = os.getenv("SCRAPER_BASE_URL", "https://example.com/jobs")


def scrape_jooble() -> List[Dict]:
    """
    Devuelve una lista de ofertas de trabajo como dicts con al menos:
    - title
    - description
    - url
    - company (opcional)
    - location (opcional)
    - source
    """
    jobs: List[Dict] = []

    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
    except Exception:
        # Si falla el scraper, devolvemos lista vacía para no romper el pipeline
        return jobs

    soup = BeautifulSoup(response.text, "html.parser")

    # Ajusta estos selectores a la estructura real de la web
    for item in soup.select(".job-card"):
        title_el = item.select_one(".job-title")
        desc_el = item.select_one(".job-description")
        company_el = item.select_one(".job-company")
        location_el = item.select_one(".job-location")
        link_el = item.select_one("a")

        title = title_el.get_text(strip=True) if title_el else "Untitled job"
        description = desc_el.get_text(strip=True) if desc_el else ""
        company = company_el.get_text(strip=True) if company_el else None
        location = location_el.get_text(strip=True) if location_el else None
        url = link_el["href"] if link_el and link_el.has_attr("href") else BASE_URL

        jobs.append(
            {
                "title": title,
                "description": description,
                "company": company,
                "location": location,
                "url": url,
                "source": "jooble",
            }
        )

    return jobs
