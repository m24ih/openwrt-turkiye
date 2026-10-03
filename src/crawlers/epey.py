import re
import time
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from curl_cffi import requests
from src.config import EPEY_IMPERSONATE

def scrape_category(session: requests.Session, category: str, max_pages: int = 25) -> List[Dict[str, Any]]:
    products = []
    print(f"[Epey] Scraping category: {category} (Max {max_pages} pages)...")
    
    for page in range(1, max_pages + 1):
        url = f"https://www.epey.com/{category}/{page}/"
        try:
            resp = session.get(url, timeout=15)
            if resp.status_code in (404, 301):
                break
            if resp.status_code != 200:
                print(f"[Epey] Status {resp.status_code} on {url}")
                break
                
            soup = BeautifulSoup(resp.text, "html.parser")
            names = []
            for a in soup.select(".detay.cell a.urunadi"):
                names.append((a.text.strip(), a.get("href", "")))
                
            prices = []
            for li in soup.select("li.fiyat.cell"):
                text = li.text.strip().replace("\n", " ")
                if "Fiyat" in text and len(text) < 10:
                    continue
                m = re.search(r"([\d\.,]+\s*TL)", text)
                prices.append(m.group(1) if m else text)
                
            if not names:
                break
                
            for idx, (name, link) in enumerate(names):
                price = prices[idx] if idx < len(prices) else ""
                products.append({
                    "name": name,
                    "link": link,
                    "price": price,
                    "source": "Epey",
                    "category": category
                })
                
            time.sleep(0.3)
        except Exception as e:
            print(f"[Epey] Error on {url}: {e}")
            break
            
    print(f"[Epey] {category}: collected {len(products)} products.")
    return products

def crawl_epey() -> List[Dict[str, Any]]:
    session = requests.Session(impersonate=EPEY_IMPERSONATE)
    categories = [
        ("router", 25),
        ("modem", 10),
        ("menzil-genisletici", 20),
        ("switch", 8)
    ]
    all_products = []
    for cat, max_p in categories:
        prods = scrape_category(session, cat, max_p)
        all_products.extend(prods)
    return all_products
