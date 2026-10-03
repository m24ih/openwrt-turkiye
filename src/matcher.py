import json
import re
import urllib.parse
from typing import List, Dict, Any
from src.config import OUTPUT_FILTERED_JSON

BRAND_MAP = {
    'tp-link': ['tp-link', 'tplink', 'tp link'],
    'xiaomi': ['xiaomi', 'redmi'],
    'cudy': ['cudy'],
    'asus': ['asus'],
    'gl.inet': ['gl.inet', 'gl-inet', 'gl inet', 'glinet'],
    'mikrotik': ['mikrotik', 'routerboard'],
    'ubiquiti': ['ubiquiti', 'unifi', 'edgerouter'],
    'zyxel': ['zyxel'],
    'mercusys': ['mercusys'],
    'd-link': ['d-link', 'dlink', 'd link'],
    'tenda': ['tenda'],
    'linksys': ['linksys'],
    'netgear': ['netgear']
}

STOPWORDS = {
    'ROUTER', 'GIGABIT', 'DUAL', 'BAND', 'WIFI', 'WI', 'FI', 'EDITION', 
    'SERIES', 'PLUS', 'PRO', 'MINI', 'OUTDOOR', 'INDOOR', 'WALL', 'SYSTEM', 
    'MESH', 'AC', 'AX', 'BE', 'N', 'V1', 'V2', 'V3', 'V4', 'V5', 'WHITE', 
    'BLACK', 'DESKTOP', 'HOME', 'GAMING', 'AP', 'RE', 'WIRELESS', 'EXTENDER',
    'MODEM', 'DSL', 'VDSL', 'ADSL', 'PORT', 'PORTS', 'MBPS', 'GBPS', 'LI', 'LU',
    'GENISLETICI', 'MENZIL', 'DAGITICI', 'KABLOSUZ', 'GUC', 'ADET', 'ACCESS', 'POINT', 'SWITCH'
}

SPECIAL_NAMES = {'HEX', 'BERYL', 'SLATE', 'OPAL', 'BRUME', 'FLINT', 'SHADOW', 'CRETA', 'CONVEXA'}

def detect_brand(text: str) -> str:
    t = text.lower()
    for b_key, aliases in BRAND_MAP.items():
        for a in aliases:
            if re.search(r'\b' + re.escape(a) + r'\b', t) or a in t:
                return b_key
    return ""

def get_alphanumeric_codes(text: str) -> set:
    t = re.sub(r'[\(\)\[\]\/,]', ' ', text)
    tokens = t.split()
    codes = set()
    for tok in tokens:
        clean = tok.strip('-_.')
        up = clean.upper()
        if up in STOPWORDS:
            continue
        if any(c.isdigit() for c in up) and len(up) >= 2:
            codes.add(up)
            for sub in up.split('-'):
                if any(c.isdigit() for c in sub) and len(sub) >= 2:
                    codes.add(sub)
        elif up in SPECIAL_NAMES:
            codes.add(up)
    return codes

def match_and_enrich(market_prods: List[Dict[str, Any]], owrt_all: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    print(f"[Matcher] Matching {len(market_prods)} market items against {len(owrt_all)} OpenWrt records...")
    
    owrt_by_brand = {}
    for entry in owrt_all:
        b_raw = entry.get('brand', '')
        b_key = detect_brand(b_raw)
        if b_key:
            owrt_by_brand.setdefault(b_key, []).append(entry)
            
    matched_results = []
    seen_links = set()
    
    for prod in market_prods:
        p_name = prod.get('name', '')
        p_link = prod.get('link', '')
        p_price = prod.get('price', '')
        
        if p_link in seen_links:
            continue
            
        p_brand = detect_brand(p_name)
        if not p_brand or p_brand not in owrt_by_brand:
            continue
            
        p_codes = get_alphanumeric_codes(p_name)
        if not p_codes:
            continue
            
        best_candidate = None
        best_score = -1
        
        for o_entry in owrt_by_brand[p_brand]:
            o_model = o_entry.get('model', '')
            if not o_model:
                continue
                
            o_codes = get_alphanumeric_codes(o_model)
            if not o_codes:
                continue
                
            exact_common = p_codes.intersection(o_codes)
            if not exact_common:
                for oc in o_codes:
                    for pc in p_codes:
                        oc_nums = re.findall(r'\d+', oc)
                        pc_nums = re.findall(r'\d+', pc)
                        if oc_nums and pc_nums and oc_nums == pc_nums:
                            if oc in pc or pc in oc:
                                exact_common.add(oc)
                                
            if not exact_common:
                continue
                
            score = sum(len(code) * 10 for code in exact_common)
            clean_om = re.sub(r'[^A-Z0-9]', '', o_model.upper())
            clean_pm = re.sub(r'[^A-Z0-9]', '', p_name.upper())
            if clean_om in clean_pm:
                score += 30
                
            v = str(o_entry.get('version', ''))
            if v and v.upper() in p_name.upper():
                score += 15
                
            rel = str(o_entry.get('supportedcurrentrel', ''))
            if rel not in ('EOL', 'None', '-', ''):
                score += 10
            if '25.' in rel:
                score += 5
            elif '24.' in rel:
                score += 4
                
            if score > best_score:
                best_score = score
                best_candidate = o_entry
                
        if best_candidate and best_score >= 15:
            seen_links.add(p_link)
            
            akakce_query = f"{best_candidate.get('brand')} {best_candidate.get('model')}"
            akakce_url = f"https://www.akakce.com/arama/?q={urllib.parse.quote_plus(akakce_query)}"
            
            ram = best_candidate.get('rammb')
            flash = best_candidate.get('flashmb')
            flash_str = ", ".join(flash) if isinstance(flash, list) else str(flash)
            
            epey_url = p_link if prod.get('source') == 'Epey' else None
            akakce_item_url = p_link if prod.get('source') == 'Akakce' else akakce_url
            if not epey_url:
                epey_url = f"https://www.epey.com/arama/?q={urllib.parse.quote_plus(akakce_query)}"
                
            matched_results.append({
                'market_title': p_name,
                'price': p_price,
                'epey_url': epey_url,
                'akakce_search_url': akakce_item_url,
                'brand': best_candidate.get('brand'),
                'model': best_candidate.get('model'),
                'version': best_candidate.get('version'),
                'supported_rel': best_candidate.get('supportedcurrentrel'),
                'cpu': best_candidate.get('cpu'),
                'ram_mb': ram,
                'flash_mb': flash_str,
                'target': f"{best_candidate.get('target', '')}/{best_candidate.get('subtarget', '')}",
                'ethernet_1g': best_candidate.get('ethernet1gports', '-'),
                'ethernet_2_5g': best_candidate.get('ethernet2_5gports', '-'),
                'wlan_hardware': best_candidate.get('wlanhardware', []),
                'device_page': f"https://openwrt.org/{best_candidate.get('devicepage')}" if best_candidate.get('devicepage') else None,
                'category': prod.get('category', 'router'),
                'wlan24ghz': best_candidate.get('wlan24ghz'),
                'wlan50ghz': best_candidate.get('wlan50ghz'),
                'wlan60ghz': best_candidate.get('wlan60ghz'),
                'usbports': best_candidate.get('usbports'),
                'bootloader': best_candidate.get('bootloader'),
                'install_url': best_candidate.get('firmwareopenwrtinstallurl'),
                'upgrade_url': best_candidate.get('firmwareopenwrtupgradeurl'),
                'install_methods': best_candidate.get('installationmethods'),
                'comments': best_candidate.get('comments'),
                'packagearchitecture': best_candidate.get('packagearchitecture'),
                'devicetype': best_candidate.get('devicetype'),
                'switch': best_candidate.get('switch')
            })

    def sort_key(d):
        pr_str = re.sub(r'[^\d]', '', d.get('price', ''))
        pr = int(pr_str) if pr_str else 99999999
        return (0 if d.get('supported_rel') != 'EOL' else 1, pr)

    matched_results.sort(key=sort_key)
    print(f"[Matcher] Found {len(matched_results)} matched unique devices.")
    
    with open(OUTPUT_FILTERED_JSON, 'w', encoding='utf-8') as f:
        json.dump(matched_results, f, ensure_ascii=False, indent=2)
    print(f"[Matcher] Saved filtered dataset to {OUTPUT_FILTERED_JSON}")
    
    return matched_results
