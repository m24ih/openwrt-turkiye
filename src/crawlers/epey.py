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
            rows = soup.select("ul.row")
            page_items = 0
            
            for row in rows:
                name_el = row.select_one(".detay.cell a.urunadi")
                if not name_el:
                    continue
                name = name_el.text.strip()
                link = name_el.get("href", "")
                
                img_el = row.select_one(".resim.cell img")
                img_url = ""
                if img_el:
                    img_url = img_el.get("src") or img_el.get("data-src") or img_el.get("data-original") or ""
                    if img_url and "/k_" in img_url:
                        img_url = img_url.replace("/k_", "/b_")
                
                price_el = row.select_one("li.fiyat.cell")
                price = ""
                if price_el:
                    text = price_el.text.strip().replace("\n", " ")
                    if not ("Fiyat" in text and len(text) < 10):
                        m = re.search(r"([\d\.,]+\s*TL)", text)
                        price = m.group(1) if m else text
                        
                products.append({
                    "name": name,
                    "link": link,
                    "price": price,
                    "image_url": img_url,
                    "source": "Epey",
                    "category": category
                })
                page_items += 1
                
            if page_items == 0:
                break
                
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
