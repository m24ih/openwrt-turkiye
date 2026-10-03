import re
import time
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from curl_cffi import requests
from src.config import AKAKCE_IMPERSONATE

def scrape_category(session: requests.Session, category: str, max_pages: int = 15) -> List[Dict[str, Any]]:
    products = []
    print(f"[Akakçe] Scraping category: {category} (Max {max_pages} pages)...")
    
    for page in range(1, max_pages + 1):
        url = f"https://www.akakce.com/{category}.html" if page == 1 else f"https://www.akakce.com/{category},{page}.html"
        try:
            resp = session.get(url, timeout=15)
            if resp.status_code in (404, 301):
                break
            if resp.status_code == 429:
                print(f"[Akakçe] Rate limited at page {page}, sleeping 5s...")
                time.sleep(5)
                continue
            if resp.status_code != 200:
                print(f"[Akakçe] Status {resp.status_code} on {url}")
                break
                
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select('a[href*="/en-ucuz-"]')
            page_items = 0
            seen_hrefs = set()
            
            for c in cards:
                href = c.get("href", "")
                if href in seen_hrefs:
                    continue
                seen_hrefs.add(href)
                
                title = c.get("title")
                if not title or len(title) < 5:
                    continue
                    
                price_match = re.search(r"([\d\.,]+\s*TL)", c.text)
                price_clean = price_match.group(1) if price_match else ""
                
                img_el = c.select_one("img")
                img_url = ""
                if img_el:
                    img_url = img_el.get("src") or img_el.get("data-src") or img_el.get("data-original") or ""
                    if img_url.startswith("//"):
                        img_url = f"https:{img_url}"
                
                full_link = f"https://www.akakce.com{href}" if href.startswith("/") else href
                products.append({
                    "name": title,
                    "link": full_link,
                    "price": price_clean,
                    "image_url": img_url,
                    "source": "Akakce",
                    "category": category
                })
                page_items += 1
                
            if page_items == 0:
                break
            time.sleep(1.0)
        except Exception as e:
            print(f"[Akakçe] Exception on {url}: {e}")
            break
            
    print(f"[Akakçe] {category}: collected {len(products)} products.")
    return products

def crawl_akakce() -> List[Dict[str, Any]]:
    session = requests.Session(impersonate=AKAKCE_IMPERSONATE)
    categories = [
        ("router", 15),
        ("modem", 8)
    ]
    all_products = []
    for cat, max_p in categories:
        prods = scrape_category(session, cat, max_p)
        all_products.extend(prods)
    return all_products
