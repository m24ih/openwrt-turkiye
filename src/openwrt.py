import json
import os
import shutil
from typing import List, Dict, Any, Tuple
from curl_cffi import requests
from src.config import OPENWRT_TOH_URL, TOH_LOCAL_FILE, EPEY_IMPERSONATE

def fetch_latest_toh() -> Tuple[List[Dict[str, Any]], bool, int]:
    """
    Downloads latest Table of Hardware from official OpenWrt source.
    Returns: (list_of_devices, has_changes, new_devices_count)
    """
    print(f"[OpenWrt] Fetching latest ToH from {OPENWRT_TOH_URL}...")
    try:
        resp = requests.get(OPENWRT_TOH_URL, impersonate=EPEY_IMPERSONATE, timeout=60)
        if resp.status_code != 200:
            print(f"[OpenWrt] Error fetching ToH: HTTP {resp.status_code}")
            return load_local_toh(), False, 0
            
        data = resp.json()
        columns = data.get("columns", [])
        entries = data.get("entries", [])
        
        latest_items = [dict(zip(columns, row)) for row in entries]
        print(f"[OpenWrt] Successfully fetched {len(latest_items)} devices from upstream.")
        
        # Compare with existing local file
        old_items = load_local_toh()
        old_count = len(old_items)
        new_count = len(latest_items)
        has_changes = old_count != new_count
        
        diff_count = max(0, new_count - old_count)
        
        if has_changes or not TOH_LOCAL_FILE.exists():
            # Backup previous
            if TOH_LOCAL_FILE.exists():
                bak = TOH_LOCAL_FILE.with_suffix(".json.bak")
                shutil.copyfile(TOH_LOCAL_FILE, bak)
                
            with open(TOH_LOCAL_FILE, "w", encoding="utf-8") as f:
                json.dump(latest_items, f, ensure_ascii=False, indent=2)
            print(f"[OpenWrt] Saved {len(latest_items)} devices to {TOH_LOCAL_FILE} (+{diff_count} new).")
        else:
            print(f"[OpenWrt] Local ToH is already up to date ({len(latest_items)} devices).")
            
        return latest_items, has_changes, diff_count
    except Exception as e:
        print(f"[OpenWrt] Exception fetching ToH: {e}")
        return load_local_toh(), False, 0

def load_local_toh() -> List[Dict[str, Any]]:
    """Loads cached OpenWrt ToH from local disk."""
    if not TOH_LOCAL_FILE.exists():
        return []
    try:
        with open(TOH_LOCAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[OpenWrt] Error reading local ToH file: {e}")
        return []
