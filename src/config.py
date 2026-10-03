import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
WEB_DIR = PROJECT_ROOT / "web"

TOH_LOCAL_FILE = RAW_DATA_DIR / "openwrt_toh_all.json"
MARKET_LOCAL_FILE = RAW_DATA_DIR / "market_products.json"
OUTPUT_FILTERED_JSON = DATA_DIR / "openwrt_turkiye.json"
OUTPUT_HTML = PROJECT_ROOT / "index.html"
WEB_HTML = WEB_DIR / "index.html"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
WEB_DIR.mkdir(parents=True, exist_ok=True)

# Upstream URLs
OPENWRT_TOH_URL = "https://toh.openwrt.org/toh.json"

# Impersonation Profiles for curl_cffi
EPEY_IMPERSONATE = "chrome120"
AKAKCE_IMPERSONATE = "chrome110"
