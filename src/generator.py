import json
import shutil
from pathlib import Path
from typing import List, Dict, Any
from src.config import PROJECT_ROOT, WEB_DIR, OUTPUT_FILTERED_JSON, OUTPUT_HTML, WEB_HTML

def generate_html(devices: List[Dict[str, Any]] = None) -> Path:
    if devices is None:
        if not OUTPUT_FILTERED_JSON.exists():
            raise FileNotFoundError(f"{OUTPUT_FILTERED_JSON} does not exist. Run update first.")
        with open(OUTPUT_FILTERED_JSON, "r", encoding="utf-8") as f:
            devices = json.load(f)

    json_data_str = json.dumps(devices, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="tr" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OpenWrt Türkiye — Ağ Cihazları Kataloğu & Fiyat Takibi</title>
  <meta name="description" content="Türkiye piyasasında (Epey & Akakçe) satışta olan OpenWrt destekli router, modem ve menzil genişleticilerin donanım özellikleri, fotoğrafları, donanım revizyon uyarıları ve kurulum kılavuzu.">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="alternate icon" href="favicon.ico">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg: #08090d;
      --surface-1: #0f1118;
      --surface-2: #151922;
      --surface-3: #1c212e;
      --surface-input: #0c0e14;
      --border: rgba(255, 255, 255, 0.08);
      --border-hover: rgba(255, 255, 255, 0.16);
      --border-active: rgba(255, 255, 255, 0.28);
      
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-subtle: #64748b;
      
      --accent: #6366f1;
      --accent-hover: #4f46e5;
      --accent-subtle: rgba(99, 102, 241, 0.12);
      --accent-border: rgba(99, 102, 241, 0.3);
      
      --success: #10b981;
      --success-subtle: rgba(16, 185, 129, 0.1);
      --success-border: rgba(16, 185, 129, 0.25);
      
      --warning: #f59e0b;
      --warning-subtle: rgba(245, 158, 11, 0.1);
      --warning-border: rgba(245, 158, 11, 0.3);
      --revision-bg: rgba(245, 158, 11, 0.08);
      --revision-border: rgba(245, 158, 11, 0.28);
      --revision-text: #fbbf24;
      --revision-bold: #fef08a;
      
      --danger: #ef4444;
      --danger-subtle: rgba(239, 68, 68, 0.1);
      --danger-border: rgba(239, 68, 68, 0.3);
      
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, monospace;
      
      --radius-sm: 6px;
      --radius-md: 8px;
      --radius-lg: 12px;
      --radius-full: 9999px;
      
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
      --shadow-md: 0 4px 16px -2px rgba(0, 0, 0, 0.4);
      --shadow-lg: 0 12px 32px -4px rgba(0, 0, 0, 0.6);
    }}

    [data-theme="light"] {{
      --bg: #f8fafc;
      --surface-1: #ffffff;
      --surface-2: #f1f5f9;
      --surface-3: #e2e8f0;
      --surface-input: #ffffff;
      --border: #e2e8f0;
      --border-hover: #cbd5e1;
      --border-active: #94a3b8;
      
      --text: #0f172a;
      --text-muted: #475569;
      --text-subtle: #64748b;
      
      --accent: #4f46e5;
      --accent-hover: #4338ca;
      --accent-subtle: rgba(79, 70, 229, 0.08);
      --accent-border: rgba(79, 70, 229, 0.25);

      --success: #059669;
      --success-subtle: rgba(5, 150, 105, 0.08);
      --success-border: rgba(5, 150, 105, 0.25);

      --warning: #b45309;
      --warning-subtle: rgba(217, 119, 6, 0.08);
      --warning-border: rgba(217, 119, 6, 0.25);

      --danger: #dc2626;
      --danger-subtle: rgba(220, 38, 38, 0.08);
      --danger-border: rgba(220, 38, 38, 0.25);

      --revision-bg: #fffbeb;
      --revision-border: rgba(217, 119, 6, 0.28);
      --revision-text: #92400e;
      --revision-bold: #78350f;
      
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 16px -2px rgba(0, 0, 0, 0.08);
      --shadow-lg: 0 12px 32px -4px rgba(0, 0, 0, 0.12);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    body {{
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    a {{ color: inherit; text-decoration: none; }}

    /* Top Navigation Bar */
    header {{
      background: var(--surface-1);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 40;
    }}

    .header-container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 0.75rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1.5rem;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }}

    .brand-logo-icon {{
      width: 28px;
      height: 28px;
      color: var(--text);
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .brand-title {{
      font-size: 1rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .badge-status {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 500;
      padding: 0.15rem 0.55rem;
      border-radius: var(--radius-full);
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--text-muted);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.4rem;
      padding: 0.4rem 0.75rem;
      font-size: 0.8125rem;
      font-weight: 500;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      background: var(--surface-1);
      color: var(--text);
      cursor: pointer;
      transition: background 0.15s, border-color 0.15s;
    }}

    .btn:hover {{
      background: var(--surface-2);
      border-color: var(--border-hover);
    }}

    .btn-primary {{
      background: var(--text);
      color: var(--bg);
      border-color: var(--text);
      font-weight: 600;
    }}

    .btn-primary:hover {{
      background: rgba(255, 255, 255, 0.9);
      border-color: rgba(255, 255, 255, 0.9);
    }}

    .btn-sm {{
      padding: 0.25rem 0.55rem;
      font-size: 0.75rem;
    }}

    /* Main Container */
    main {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      flex: 1;
      width: 100%;
    }}

    /* Hero Section */
    .hero {{
      margin-bottom: 2rem;
    }}

    .hero-eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 0.4rem;
    }}

    .hero-heading {{
      font-size: 2rem;
      font-weight: 700;
      letter-spacing: -0.035em;
      line-height: 1.2;
      color: var(--text);
      margin-bottom: 0.5rem;
    }}

    .hero-desc {{
      font-size: 0.9375rem;
      color: var(--text-muted);
      max-width: 780px;
      line-height: 1.5;
    }}

    /* Metrics Strip */
    .metrics-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      margin: 1.75rem 0;
    }}

    .metric-card {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 1rem 1.25rem;
      box-shadow: var(--shadow-sm);
    }}

    .metric-label {{
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--text-subtle);
      margin-bottom: 0.35rem;
      letter-spacing: 0.01em;
    }}

    .metric-value {{
      font-family: var(--font-mono);
      font-size: 1.75rem;
      font-weight: 600;
      letter-spacing: -0.03em;
      color: var(--text);
    }}

    .metric-note {{
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-top: 0.2rem;
    }}

    /* Featured models strip */
    .featured-bar {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 1.75rem;
      padding: 0.65rem 0.85rem;
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow-x: auto;
      scrollbar-width: none;
    }}

    .featured-label {{
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-subtle);
      white-space: nowrap;
      margin-right: 0.25rem;
    }}

    .featured-tag {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.25rem 0.65rem;
      border-radius: var(--radius-full);
      background: var(--surface-2);
      border: 1px solid var(--border);
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--text);
      cursor: pointer;
      white-space: nowrap;
      transition: border-color 0.15s, background 0.15s;
    }}

    .featured-tag:hover {{
      border-color: var(--border-hover);
      background: var(--surface-3);
    }}

    .featured-tag code {{
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      color: var(--text-muted);
    }}

    /* Filter Toolbelt */
    .filter-panel {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 1rem 1.25rem;
      margin-bottom: 1.5rem;
      box-shadow: var(--shadow-sm);
    }}

    .filter-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.75rem;
    }}

    .search-input-wrap {{
      flex: 1;
      min-width: 260px;
      position: relative;
      display: flex;
      align-items: center;
    }}

    .search-input-wrap svg {{
      position: absolute;
      left: 0.85rem;
      width: 15px;
      height: 15px;
      color: var(--text-subtle);
      pointer-events: none;
    }}

    .search-input {{
      width: 100%;
      padding: 0.55rem 2.4rem 0.55rem 2.3rem;
      background: var(--surface-input);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      color: var(--text);
      font-family: var(--font-sans);
      font-size: 0.875rem;
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }}

    .search-input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 1px var(--accent);
    }}

    .kbd-shortcut {{
      position: absolute;
      right: 0.75rem;
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      color: var(--text-subtle);
      padding: 0.1rem 0.35rem;
      border-radius: 4px;
      background: var(--surface-2);
      border: 1px solid var(--border);
      pointer-events: none;
    }}

    .filter-select {{
      background: var(--surface-input);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 0.55rem 0.75rem;
      border-radius: var(--radius-sm);
      font-family: var(--font-sans);
      font-size: 0.8125rem;
      font-weight: 500;
      outline: none;
      cursor: pointer;
      transition: border-color 0.15s;
    }}

    .filter-select:hover {{
      border-color: var(--border-hover);
    }}

    .filter-select:focus {{
      border-color: var(--accent);
    }}

    /* Brands scrollable list */
    .brand-chips-wrap {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      margin-top: 0.85rem;
      padding-top: 0.85rem;
      border-top: 1px solid var(--border);
    }}

    .brand-chip {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 500;
      padding: 0.2rem 0.55rem;
      border-radius: var(--radius-sm);
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s;
      user-select: none;
    }}

    .brand-chip:hover {{
      color: var(--text);
      border-color: var(--border-hover);
    }}

    .brand-chip.active {{
      background: var(--text);
      color: var(--bg);
      border-color: var(--text);
      font-weight: 600;
    }}

    /* Results Header Bar */
    .results-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1.25rem;
      padding: 0 0.25rem;
    }}

    .results-count {{
      font-size: 0.8125rem;
      color: var(--text-muted);
    }}

    .results-count b {{
      font-family: var(--font-mono);
      color: var(--text);
    }}

    .view-switch {{
      display: flex;
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      overflow: hidden;
    }}

    .view-switch-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.35rem 0.65rem;
      font-size: 0.75rem;
      font-weight: 500;
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      transition: color 0.15s, background 0.15s;
    }}

    .view-switch-btn.active {{
      background: var(--surface-2);
      color: var(--text);
    }}

    /* Device Cards Grid */
    .devices-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 1.25rem;
    }}

    .device-card {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: border-color 0.15s, transform 0.15s;
      box-shadow: var(--shadow-sm);
      position: relative;
    }}

    .device-card:hover {{
      border-color: var(--border-hover);
      transform: translateY(-2px);
    }}

    .card-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      margin-bottom: 0.5rem;
    }}

    .brand-badge {{
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      font-weight: 600;
      color: var(--text-subtle);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .pill-release {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      font-weight: 500;
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-full);
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--text-muted);
    }}

    .pill-release.active {{
      background: var(--success-subtle);
      border-color: var(--success-border);
      color: var(--success);
    }}

    .pill-release.active::before {{
      content: '';
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--success);
    }}

    .pill-release.eol {{
      background: var(--danger-subtle);
      border-color: rgba(239, 68, 68, 0.25);
      color: var(--danger);
    }}

    /* Router Photo Thumbnail in Card */
    .card-thumb-wrap {{
      width: 100%;
      height: 140px;
      background: #ffffff;
      border-radius: var(--radius-md);
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0.6rem 0 0.85rem;
      overflow: hidden;
      position: relative;
      padding: 0.65rem;
    }}

    .card-thumb-img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      transition: transform 0.2s ease;
    }}

    .device-card:hover .card-thumb-img {{
      transform: scale(1.05);
    }}

    .card-thumb-fallback {{
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--surface-2);
      color: var(--text-subtle);
    }}

    .card-thumb-fallback svg {{
      width: 44px;
      height: 44px;
      opacity: 0.5;
    }}

    .card-model {{
      font-size: 1.125rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text);
      line-height: 1.3;
      margin-bottom: 0.25rem;
    }}

    .card-market-name {{
      font-size: 0.8125rem;
      color: var(--text-muted);
      margin-bottom: 0.75rem;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      line-height: 1.4;
      min-height: 2.25rem;
    }}

    .card-price-row {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 0.85rem;
      padding-bottom: 0.65rem;
      border-bottom: 1px solid var(--border);
    }}

    .price-value {{
      font-family: var(--font-mono);
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text);
    }}

    .price-none {{
      font-size: 0.8125rem;
      color: var(--text-subtle);
    }}

    /* Hardware Specs Matrix */
    .specs-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.5rem;
      background: var(--surface-input);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 0.65rem 0.75rem;
      margin-bottom: 0.75rem;
    }}

    .spec-cell {{
      display: flex;
      flex-direction: column;
    }}

    .spec-key {{
      font-family: var(--font-mono);
      font-size: 0.65rem;
      font-weight: 500;
      color: var(--text-subtle);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .spec-val {{
      font-family: var(--font-mono);
      font-size: 0.78125rem;
      font-weight: 600;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    /* Install Method & Revision Badges */
    .card-badges-row {{
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      margin-bottom: 1rem;
    }}

    .install-method-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      font-weight: 500;
      padding: 0.25rem 0.55rem;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      width: fit-content;
    }}

    .install-method-badge.success {{
      background: var(--success-subtle);
      border-color: var(--success-border);
      color: var(--success);
    }}

    .install-method-badge.warning {{
      background: var(--warning-subtle);
      border-color: var(--warning-border);
      color: var(--warning);
    }}

    .install-method-badge.info {{
      background: var(--accent-subtle);
      border-color: var(--accent-border);
      color: var(--accent);
    }}

    .install-method-badge.danger {{
      background: var(--danger-subtle);
      border-color: var(--danger-border);
      color: var(--danger);
    }}

    .install-method-badge.default {{
      background: var(--surface-2);
      border-color: var(--border);
      color: var(--text-muted);
    }}

    .revision-box {{
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      padding: 0.35rem 0.65rem;
      border-radius: var(--radius-sm);
      background: var(--revision-bg);
      border: 1px solid var(--revision-border);
      color: var(--revision-text);
      display: flex;
      align-items: center;
      gap: 0.45rem;
      line-height: 1.35;
    }}

    .revision-box b {{
      color: var(--revision-bold);
      font-weight: 700;
    }}

    .card-footer-actions {{
      display: flex;
      gap: 0.5rem;
      margin-top: auto;
    }}

    .card-footer-actions .btn {{
      flex: 1;
      padding: 0.35rem 0.5rem;
      font-size: 0.75rem;
    }}

    .card-links-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 0.75rem;
      padding-top: 0.75rem;
      border-top: 1px solid var(--border);
      font-size: 0.75rem;
      color: var(--text-muted);
    }}

    .card-links-row a:hover {{
      color: var(--text);
      text-decoration: underline;
    }}

    /* Table View */
    .table-container {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow-x: auto;
      box-shadow: var(--shadow-sm);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8125rem;
      text-align: left;
    }}

    th {{
      background: var(--surface-2);
      padding: 0.75rem 1rem;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-subtle);
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    }}

    th:hover {{
      color: var(--text);
    }}

    td {{
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tr:hover {{
      background: var(--surface-2);
    }}

    .table-device-cell {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}

    .table-thumb {{
      width: 40px;
      height: 40px;
      border-radius: var(--radius-sm);
      background: #ffffff;
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      flex-shrink: 0;
      padding: 2px;
    }}

    .table-thumb img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }}

    .table-thumb-fallback {{
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--surface-2);
      color: var(--text-subtle);
    }}

    /* Detail Modal */
    dialog {{
      margin: auto;
      max-width: 640px;
      width: 90%;
      background: var(--surface-1);
      color: var(--text);
      border: 1px solid var(--border-hover);
      border-radius: var(--radius-lg);
      padding: 1.5rem;
      box-shadow: var(--shadow-lg);
    }}

    dialog::backdrop {{
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(6px);
    }}

    .modal-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 1rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid var(--border);
    }}

    .modal-close-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      padding: 0.25rem;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: var(--radius-sm);
    }}

    .modal-close-btn:hover {{
      color: var(--text);
      background: var(--surface-2);
    }}

    .modal-photo-wrap {{
      width: 100%;
      height: 200px;
      background: #ffffff;
      border-radius: var(--radius-md);
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 1.25rem;
      overflow: hidden;
      padding: 1rem;
    }}

    .modal-photo-wrap img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }}

    .modal-warning-box {{
      background: var(--revision-bg);
      border: 1px solid var(--revision-border);
      border-radius: var(--radius-md);
      padding: 0.85rem;
      font-size: 0.8125rem;
      color: var(--revision-text);
      margin-bottom: 1rem;
      line-height: 1.5;
    }}

    .modal-warning-box b {{
      color: var(--revision-bold);
      font-weight: 700;
    }}

    .modal-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
      margin-bottom: 1.25rem;
    }}

    .modal-field {{
      display: flex;
      flex-direction: column;
    }}

    .modal-key {{
      font-family: var(--font-mono);
      font-size: 0.6875rem;
      color: var(--text-subtle);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 0.15rem;
    }}

    .modal-val {{
      font-family: var(--font-mono);
      font-size: 0.8125rem;
      font-weight: 500;
      color: var(--text);
      word-break: break-all;
    }}

    .modal-note-box {{
      background: var(--surface-input);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 0.75rem;
      font-size: 0.8125rem;
      color: var(--text-muted);
      margin-bottom: 1.25rem;
      line-height: 1.5;
    }}

    .modal-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}

    /* Footer */
    footer {{
      margin-top: auto;
      background: var(--surface-1);
      border-top: 1px solid var(--border);
      padding: 1.5rem;
      text-align: center;
      color: var(--text-subtle);
      font-size: 0.8125rem;
    }}

    .footer-links {{
      display: flex;
      justify-content: center;
      gap: 1.25rem;
      margin-bottom: 0.5rem;
      font-family: var(--font-mono);
      font-size: 0.75rem;
    }}

    @media (max-width: 860px) {{
      .metrics-grid {{ grid-template-columns: repeat(2, 1fr); }}
      .header-container {{ flex-direction: column; align-items: flex-start; gap: 0.75rem; }}
      .header-actions {{ width: 100%; justify-content: flex-end; }}
    }}
    
    @media (max-width: 520px) {{
      .metrics-grid {{ grid-template-columns: 1fr; }}
      .devices-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <header>
    <div class="header-container">
      <div class="brand-wrap">
        <a href="#" class="brand-title">
          <img src="favicon.svg" alt="OpenWrt" class="brand-logo-icon" width="28" height="28">
          OpenWrt Türkiye
        </a>
        <span class="badge-status">v24.x · v25.x Kataloğu</span>
      </div>

      <div class="header-actions">
        <button id="themeToggle" class="btn" title="Tema Değiştir">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
          <span>Tema</span>
        </button>
        <button id="exportBtn" class="btn" title="JSON İndir">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          <span>JSON</span>
        </button>
        <button id="exportCsvBtn" class="btn" title="CSV İndir">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
          <span>CSV</span>
        </button>
        <a href="https://github.com/m24ih/openwrt-turkiye/issues/new/choose" target="_blank" class="btn" title="Sorun veya Hatalı Eşleşme Bildir">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>Sorun Bildir</span>
        </a>
        <a href="https://github.com/m24ih/openwrt-turkiye" target="_blank" class="btn" title="GitHub Deposu">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
          </svg>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="hero-eyebrow">Haftalık Otomatik Pazar & ToH Senkronizasyonu</div>
      <h1 class="hero-heading">Türkiye'de Satışta Olan OpenWrt Cihazları</h1>
      <p class="hero-desc">OpenWrt resmi donanım veritabanı (ToH) ile Epey ve Akakçe Türkiye piyasası çapraz eşleştirmesi. Satın alınabilir router modelleri, donanım mimarileri, revizyon uyarıları ve kurulum yöntemleri.</p>

      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-label">Eşleşen Cihaz</div>
          <div class="metric-value" id="statTotal">-</div>
          <div class="metric-note">Türkiye pazarında satışta</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Aktif Desteklenen</div>
          <div class="metric-value" id="statActive" style="color: var(--success);">-</div>
          <div class="metric-note">OpenWrt 24.x ve 25.x</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Wi-Fi 6 (802.11ax)</div>
          <div class="metric-value" id="statWifi6" style="color: var(--accent);">-</div>
          <div class="metric-note">Yeni nesil yüksek hız</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Piyasa Fiyatı Olan</div>
          <div class="metric-value" id="statPriced">-</div>
          <div class="metric-note">Anlık pazar kayıtlı</div>
        </div>
      </div>

      <div class="featured-bar">
        <span class="featured-label">Öne Çıkanlar</span>
        <span class="featured-tag" onclick="quickFilter('WR3000')">Cudy WR3000 <code>Kolay Web Flash</code></span>
        <span class="featured-tag" onclick="quickFilter('AX3000T')">Xiaomi AX3000T <code>Sadece RD23/RD03</code></span>
        <span class="featured-tag" onclick="quickFilter('4A Gigabit')">Xiaomi 4A Gigabit <code>Exploit ile</code></span>
        <span class="featured-tag" onclick="quickFilter('X6')">Cudy X6 <code>AX1800</code></span>
        <span class="featured-tag" onclick="quickFilter('hEX S')">MikroTik hEX S <code>Kablolu</code></span>
        <span class="featured-tag" onclick="quickFilter('Beryl')">GL.iNet Beryl AX <code>Kolay Web Flash</code></span>
      </div>
    </section>

    <section class="filter-panel">
      <div class="filter-row">
        <div class="search-input-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" id="searchInput" class="search-input" placeholder="Marka, model, işlemci veya revizyon ara (örn. MT7981, v2, WR3000)...">
          <span class="kbd-shortcut">/</span>
        </div>

        <select id="methodFilter" class="filter-select">
          <option value="ALL">Kurulum: Tümü</option>
          <option value="EASY">Kolay Web Arayüzü</option>
          <option value="EXPLOIT">Yazılım Açığı (Exploit / SSH)</option>
          <option value="TFTP">TFTP / Ağ Kurtarma</option>
          <option value="SERIAL">Seri Port (UART)</option>
        </select>

        <select id="wifiFilter" class="filter-select">
          <option value="ALL">Wi-Fi Standartı: Tümü</option>
          <option value="WIFI6">Wi-Fi 6 (802.11ax)</option>
          <option value="WIFI5">Wi-Fi 5 (802.11ac)</option>
          <option value="WIFI4">Wi-Fi 4 (802.11n)</option>
          <option value="ETHERNET">Kablolu Router (Wi-Fi Yok)</option>
        </select>

        <select id="statusFilter" class="filter-select">
          <option value="ACTIVE" selected>Durum: Sadece Aktif Destek</option>
          <option value="ALL">Durum: Tümü (EOL Dahil)</option>
          <option value="25">En Güncel (OpenWrt 25.x)</option>
          <option value="24">OpenWrt 24.x</option>
          <option value="EOL">Yalnızca EOL (Destek Bitti)</option>
        </select>

        <select id="ramFilter" class="filter-select">
          <option value="0">RAM: Tümü</option>
          <option value="128">≥ 128 MB RAM</option>
          <option value="256">≥ 256 MB RAM</option>
          <option value="512">≥ 512 MB RAM</option>
        </select>

        <select id="flashFilter" class="filter-select">
          <option value="0">Flash: Tümü</option>
          <option value="16">≥ 16 MB Flash</option>
          <option value="32">≥ 32 MB Flash</option>
          <option value="128">≥ 128 MB Flash</option>
        </select>

        <select id="sortSelect" class="filter-select">
          <option value="PRICE_ASC">Fiyat: Artan (En Ucuz)</option>
          <option value="PRICE_DESC">Fiyat: Azalan (En Pahalı)</option>
          <option value="NAME_ASC">Model Adı (A-Z)</option>
          <option value="RAM_DESC">RAM: En Yüksek</option>
          <option value="REL_DESC">En Yeni Sürüm</option>
        </select>
      </div>

      <div class="brand-chips-wrap" id="brandChips"></div>
    </section>

    <div class="results-bar">
      <div class="results-count" id="resultsCount">Yükleniyor...</div>
      <div class="view-switch">
        <button class="view-switch-btn active" id="btnViewGrid" onclick="setViewMode('grid')">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Kartlar</span>
        </button>
        <button class="view-switch-btn" id="btnViewTable" onclick="setViewMode('table')">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <line x1="3" y1="6" x2="3.01" y2="6"></line>
            <line x1="3" y1="12" x2="3.01" y2="12"></line>
            <line x1="3" y1="18" x2="3.01" y2="18"></line>
          </svg>
          <span>Tablo</span>
        </button>
      </div>
    </div>

    <div id="gridContainer" class="devices-grid"></div>

    <div id="tableContainer" class="table-container" style="display: none;">
      <table>
        <thead>
          <tr>
            <th onclick="sortTable('brand')">Cihaz</th>
            <th onclick="sortTable('price')">Fiyat</th>
            <th>Kurulum Yöntemi</th>
            <th>Revizyon</th>
            <th onclick="sortTable('supported_rel')">Sürüm</th>
            <th onclick="sortTable('cpu')">İşlemci (SoC)</th>
            <th onclick="sortTable('ram_mb')">RAM</th>
            <th onclick="sortTable('flash_mb')">Flash</th>
            <th>Bağlantılar</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </main>

  <dialog id="detailModal">
    <div class="modal-head">
      <div>
        <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-subtle); text-transform: uppercase;" id="modalBrand">Brand</div>
        <div style="font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; margin-top: 0.15rem;" id="modalTitle">Model</div>
      </div>
      <button class="modal-close-btn" onclick="closeModal()" title="Kapat">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <div class="modal-photo-wrap" id="modalPhotoWrap">
      <img id="modalPhoto" src="" alt="" loading="lazy">
    </div>

    <div id="modalWarningWrap" style="display: none;">
      <div class="modal-warning-box" id="modalWarningText"></div>
    </div>

    <div class="modal-grid" id="modalDetails"></div>

    <div style="font-family: var(--font-mono); font-size: 0.6875rem; color: var(--text-subtle); text-transform: uppercase; margin-bottom: 0.35rem;">Topluluk Notu & Kurulum Bilgisi</div>
    <div class="modal-note-box" id="modalComments"></div>

    <div class="modal-actions" id="modalLinks"></div>
  </dialog>

  <footer>
    <div class="footer-links">
      <a href="https://openwrt.org" target="_blank">openwrt.org</a>
      <span>·</span>
      <a href="https://epey.com" target="_blank">epey.com</a>
      <span>·</span>
      <a href="https://akakce.com" target="_blank">akakce.com</a>
      <span>·</span>
      <a href="https://github.com/m24ih/openwrt-turkiye" target="_blank">github.com/m24ih/openwrt-turkiye</a>
    </div>
    <p>OpenWrt Türkiye Kataloğu — Açık kaynak kodlu ve bağımsız topluluk projesidir.</p>
  </footer>

  <script>
    const RAW_DEVICES = {json_data_str};
    let currentBrand = 'ALL';
    let currentView = 'grid';
    let filteredList = [];

    RAW_DEVICES.forEach(d => {{
      const numStr = (d.price || '').replace(/[^0-9]/g, '');
      d.priceNum = numStr ? parseInt(numStr, 10) : 99999999;
      d.ramNum = d.ram_mb ? parseInt(d.ram_mb, 10) : 0;
      const fStr = (d.flash_mb || '').replace(/[^0-9]/g, '');
      d.flashNum = fStr ? parseInt(fStr, 10) : 0;
    }});

    function getInstallMethodInfo(d) {{
      const brand = (d.brand || '').toLowerCase();
      const model = (d.model || '').toLowerCase();
      const methods = d.install_methods || [];
      const mStr = (Array.isArray(methods) ? methods.join(' ') : String(methods)).toLowerCase();
      const comments = String(d.comments || '').toLowerCase();

      // Xiaomi / Redmi exploit / script uyarısı
      if (brand.includes('xiaomi') || brand.includes('redmi')) {{
        if (!brand.includes('cudy')) {{
          return {{
            key: 'EXPLOIT',
            label: 'Yazılım Açığı (Exploit / SSH)',
            type: 'warning',
            desc: 'Stok arayüz üçüncü parti yazılıma kilitlidir; Python exploit (OpenWRTInvasion/XMir) veya SSH enjeksiyonu gerektirir.'
          }};
        }}
      }}

      if (mStr.includes('serial') || mStr.includes('uart') || comments.includes('serial recovery')) {{
        return {{
          key: 'SERIAL',
          label: 'Seri Port (UART / Lehim)',
          type: 'danger',
          desc: 'Cihaz kasasının açılarak UART/seri kablo bağlanmasını gerektirebilir.'
        }};
      }}

      if (mStr.includes('gui oem') || mStr.includes('gui generic') || mStr.includes('gl.inet') || mStr.includes('d-link recovery gui')) {{
        return {{
          key: 'EASY',
          label: 'Kolay Web Arayüzü',
          type: 'success',
          desc: 'Orijinal web yönetim panelinden dosya seçilerek doğrudan firmware yüklenebilir.'
        }};
      }}

      if (mStr.includes('tftp') || mStr.includes('recovery') || mStr.includes('restoration') || mStr.includes('cfe')) {{
        return {{
          key: 'TFTP',
          label: 'TFTP / Ağ Kurtarma',
          type: 'info',
          desc: 'Ağ kablosu ve bilgisayarda TFTP sunucusu açılarak bootloader aşamasında firmware yüklenir.'
        }};
      }}

      return {{
        key: 'OTHER',
        label: 'Standart / Wiki Takibi',
        type: 'default',
        desc: 'Resmi OpenWrt Wiki sayfasındaki cihaza özel kurulum adımlarını takip ediniz.'
      }};
    }}

    function formatVersion(v) {{
      if (!v) return null;
      if (Array.isArray(v)) {{
        if (v.length === 1) return v[0];
        if (v.length <= 3) return v.join(', ');
        const first = v[0];
        if (first.startsWith('v')) {{
          const major = first.substring(0, 2);
          if (v.every(x => x.startsWith(major))) {{
            return `${{major}}.x (${{v.length}} alt revizyon)`;
          }}
        }}
        return `${{v[0]}}, ${{v[1]}} (+${{v.length - 2}} rev.)`;
      }}
      return String(v);
    }}

    function init() {{
      renderStats();
      renderBrandChips();
      setupEventListeners();
      applyFilters();
    }}

    function renderStats() {{
      const total = RAW_DEVICES.length;
      const active = RAW_DEVICES.filter(d => d.supported_rel !== 'EOL' && d.supported_rel !== '-').length;
      const wifi6 = RAW_DEVICES.filter(d => {{
        const cpu = (d.cpu || '').toUpperCase();
        const model = (d.model || '').toUpperCase();
        const title = (d.market_title || '').toUpperCase();
        return model.includes('AX') || title.includes('AX') || cpu.includes('7981') || cpu.includes('7986') || cpu.includes('IPQ50') || cpu.includes('IPQ807') || model.includes('BE');
      }}).length;
      const priced = RAW_DEVICES.filter(d => d.price && d.price.includes('TL')).length;

      document.getElementById('statTotal').innerText = total;
      document.getElementById('statActive').innerText = active;
      document.getElementById('statWifi6').innerText = wifi6;
      document.getElementById('statPriced').innerText = priced;
    }}

    function renderBrandChips() {{
      const brandCounts = {{}};
      RAW_DEVICES.forEach(d => {{
        const b = d.brand || 'Diğer';
        brandCounts[b] = (brandCounts[b] || 0) + 1;
      }});

      const sortedBrands = Object.entries(brandCounts).sort((a, b) => b[1] - a[1]);
      const container = document.getElementById('brandChips');
      
      let html = `<button class="brand-chip active" onclick="setBrand('ALL')">Tümü (${{RAW_DEVICES.length}})</button>`;
      sortedBrands.forEach(([brand, count]) => {{
        html += `<button class="brand-chip" id="chip-${{brand.replace(/[^a-zA-Z0-9]/g, '')}}" onclick="setBrand('${{brand}}')">${{brand}} (${{count}})</button>`;
      }});
      container.innerHTML = html;
    }}

    function setBrand(brand) {{
      currentBrand = brand;
      document.querySelectorAll('.brand-chip').forEach(btn => btn.classList.remove('active'));
      if (brand === 'ALL') {{
        document.querySelector('.brand-chip').classList.add('active');
      }} else {{
        const el = document.getElementById('chip-' + brand.replace(/[^a-zA-Z0-9]/g, ''));
        if (el) el.classList.add('active');
      }}
      applyFilters();
    }}

    function quickFilter(term) {{
      document.getElementById('searchInput').value = term;
      document.getElementById('statusFilter').value = 'ALL';
      document.getElementById('methodFilter').value = 'ALL';
      setBrand('ALL');
      applyFilters();
    }}

    function setupEventListeners() {{
      document.getElementById('searchInput').addEventListener('input', applyFilters);
      document.getElementById('methodFilter').addEventListener('change', applyFilters);
      document.getElementById('wifiFilter').addEventListener('change', applyFilters);
      document.getElementById('statusFilter').addEventListener('change', applyFilters);
      document.getElementById('ramFilter').addEventListener('change', applyFilters);
      document.getElementById('flashFilter').addEventListener('change', applyFilters);
      document.getElementById('sortSelect').addEventListener('change', applyFilters);

      window.addEventListener('keydown', (e) => {{
        if (e.key === '/' && document.activeElement !== document.getElementById('searchInput')) {{
          e.preventDefault();
          document.getElementById('searchInput').focus();
        }}
        if (e.key === 'Escape') {{
          const dialog = document.getElementById('detailModal');
          if (dialog.open) {{
            dialog.close();
          }} else if (document.getElementById('searchInput').value) {{
            document.getElementById('searchInput').value = '';
            applyFilters();
          }}
        }}
      }});

      document.getElementById('themeToggle').addEventListener('click', () => {{
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
      }});

      document.getElementById('exportBtn').addEventListener('click', () => {{
        const blob = new Blob([JSON.stringify(filteredList, null, 2)], {{ type: 'application/json' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'OpenWrt_Turkiye_Filtreli.json';
        a.click();
      }});

      document.getElementById('exportCsvBtn').addEventListener('click', exportCsv);
    }}

    function exportCsv() {{
      if (!filteredList.length) return;
      const headers = ['Marka', 'Model', 'Piyasa Adi', 'Fiyat', 'Revizyon', 'Kurulum Yontemi', 'Fotoğraf', 'OpenWrt Surumu', 'CPU', 'RAM (MB)', 'Flash (MB)', 'Hedef Mimari', 'Epey Linki', 'Akakce Linki', 'OpenWrt ToH'];
      const rows = filteredList.map(d => {{
        const mInfo = getInstallMethodInfo(d);
        const vStr = formatVersion(d.version) || '';
        return [
          '"' + (d.brand || '') + '"',
          '"' + (d.model || '') + '"',
          '"' + (d.market_title || '') + '"',
          '"' + (d.price || '') + '"',
          '"' + vStr + '"',
          '"' + mInfo.label + '"',
          '"' + (d.image_url || '') + '"',
          '"' + (d.supported_rel || '') + '"',
          '"' + (d.cpu || '') + '"',
          '"' + (d.ram_mb || '') + '"',
          '"' + (d.flash_mb || '') + '"',
          '"' + (d.target || '') + '"',
          '"' + (d.epey_url || '') + '"',
          '"' + (d.akakce_search_url || '') + '"',
          '"' + (d.device_page || '') + '"'
        ];
      }});
      const csvContent = '\\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'OpenWrt_Turkiye_Listesi.csv';
      a.click();
    }}

    function applyFilters() {{
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const method = document.getElementById('methodFilter').value;
      const wifi = document.getElementById('wifiFilter').value;
      const status = document.getElementById('statusFilter').value;
      const minRam = parseInt(document.getElementById('ramFilter').value, 10);
      const minFlash = parseInt(document.getElementById('flashFilter').value, 10);
      const sort = document.getElementById('sortSelect').value;

      filteredList = RAW_DEVICES.filter(d => {{
        if (currentBrand !== 'ALL' && d.brand !== currentBrand) return false;
        
        const mInfo = getInstallMethodInfo(d);
        if (method !== 'ALL' && mInfo.key !== method) return false;

        if (q) {{
          const vStr = formatVersion(d.version) || '';
          const haystack = `${{d.brand}} ${{d.model}} ${{d.market_title}} ${{d.cpu}} ${{d.target}} ${{d.supported_rel}} ${{vStr}} ${{mInfo.label}}`.toLowerCase();
          if (!haystack.includes(q)) return false;
        }}
        if (status === 'ACTIVE' && (d.supported_rel === 'EOL' || d.supported_rel === '-')) return false;
        if (status === '25' && !(d.supported_rel || '').startsWith('25.')) return false;
        if (status === '24' && !(d.supported_rel || '').startsWith('24.')) return false;
        if (status === 'EOL' && d.supported_rel !== 'EOL') return false;

        if (minRam > 0 && d.ramNum < minRam) return false;
        if (minFlash > 0 && d.flashNum < minFlash) return false;

        if (wifi !== 'ALL') {{
          const model = (d.model || '').toUpperCase();
          const title = (d.market_title || '').toUpperCase();
          const cpu = (d.cpu || '').toUpperCase();
          const isAx = model.includes('AX') || title.includes('AX') || cpu.includes('7981') || cpu.includes('7986') || cpu.includes('IPQ50') || cpu.includes('IPQ807') || model.includes('BE') || title.includes('BE');
          const isAc = model.includes('AC') || title.includes('AC') || cpu.includes('7621') || cpu.includes('7628') || cpu.includes('QCA95') || model.includes('C6') || model.includes('C7') || model.includes('WR1300');
          const isN = model.includes('N') || title.includes('N') || cpu.includes('7240') || cpu.includes('9342');
          
          if (wifi === 'WIFI6' && !isAx) return false;
          if (wifi === 'WIFI5' && !isAc) return false;
          if (wifi === 'WIFI4' && !isN) return false;
          if (wifi === 'ETHERNET' && (isAx || isAc || isN)) return false;
        }}

        return true;
      }});

      // Sıralama Mantığı: Fiyatı Listelenmeyenler HER ZAMAN listenin en altına gider!
      filteredList.sort((a, b) => {{
        const aHasPrice = a.price && a.price.includes('TL');
        const bHasPrice = b.price && b.price.includes('TL');

        if (aHasPrice && !bHasPrice) return -1;
        if (!aHasPrice && bHasPrice) return 1;

        if (sort === 'PRICE_ASC') return a.priceNum - b.priceNum;
        if (sort === 'PRICE_DESC') return b.priceNum - a.priceNum;
        if (sort === 'NAME_ASC') return (a.model || '').localeCompare(b.model || '');
        if (sort === 'RAM_DESC') return b.ramNum - a.ramNum;
        if (sort === 'REL_DESC') return (b.supported_rel || '').localeCompare(a.supported_rel || '');
        return 0;
      }});

      document.getElementById('resultsCount').innerHTML = `Bulunan Sonuç: <b>${{filteredList.length}}</b> cihaz`;

      if (currentView === 'grid') renderGrid();
      else renderTable();
    }}

    function setViewMode(mode) {{
      currentView = mode;
      document.getElementById('btnViewGrid').classList.toggle('active', mode === 'grid');
      document.getElementById('btnViewTable').classList.toggle('active', mode === 'table');
      document.getElementById('gridContainer').style.display = mode === 'grid' ? 'grid' : 'none';
      document.getElementById('tableContainer').style.display = mode === 'table' ? 'block' : 'none';
      if (mode === 'grid') renderGrid();
      else renderTable();
    }}

    function getReleasePill(rel) {{
      if (!rel || rel === '-') return `<span class="pill-release">-</span>`;
      if (rel === 'EOL') return `<span class="pill-release eol">EOL</span>`;
      if (rel === 'snapshot') return `<span class="pill-release">snapshot</span>`;
      return `<span class="pill-release active">v${{rel}}</span>`;
    }}

    function renderGrid() {{
      const container = document.getElementById('gridContainer');
      if (!filteredList.length) {{
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem; color: var(--text-subtle);">
          <div style="font-size: 1.125rem; font-weight: 600; color: var(--text);">Kriterlere uygun cihaz bulunamadı</div>
          <p style="margin-top: 0.35rem; font-size: 0.875rem;">Arama terimini temizleyebilir veya filtre ayarlarını sıfırlayabilirsiniz.</p>
        </div>`;
        return;
      }}

      let html = '';
      filteredList.forEach((d, idx) => {{
        const hasPrice = d.price && d.price.includes('TL');
        const priceHtml = hasPrice 
          ? `<span class="price-value">${{d.price}}</span>` 
          : `<span class="price-none">Fiyat Listelenmiyor</span>`;

        const hasImg = !!d.image_url;
        const imgMarkup = hasImg 
          ? `<img src="${{d.image_url}}" alt="${{d.model || d.market_title}}" class="card-thumb-img" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">`
          : '';
        const fallbackStyle = hasImg ? 'style="display:none;"' : '';

        const mInfo = getInstallMethodInfo(d);
        const versionStr = formatVersion(d.version);

        html += `
          <div class="device-card">
            <div>
              <div class="card-top">
                <span class="brand-badge">${{d.brand || 'Diğer'}}</span>
                ${{getReleasePill(d.supported_rel)}}
              </div>
              
              <div class="card-thumb-wrap">
                ${{imgMarkup}}
                <div class="card-thumb-fallback" ${{fallbackStyle}}>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="2" y="13" width="20" height="8" rx="2"></rect>
                    <path d="M6 13V8a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v5"></path>
                    <line x1="6" y1="17" x2="6.01" y2="17"></line>
                    <line x1="10" y1="17" x2="10.01" y2="17"></line>
                    <line x1="14" y1="17" x2="14.01" y2="17"></line>
                    <line x1="18" y1="17" x2="18.01" y2="17"></line>
                    <line x1="12" y1="6" x2="12" y2="3"></line>
                  </svg>
                </div>
              </div>

              <div class="card-model">${{d.model || d.market_title}}</div>
              <div class="card-market-name" title="${{d.market_title}}">${{d.market_title}}</div>

              <div class="card-price-row">
                ${{priceHtml}}
                <span style="font-family: var(--font-mono); font-size: 0.6875rem; color: var(--text-subtle);">${{d.target || ''}}</span>
              </div>

              <div class="specs-grid">
                <div class="spec-cell">
                  <span class="spec-key">İşlemci</span>
                  <span class="spec-val" title="${{d.cpu || '-'}}">${{d.cpu || '-'}}</span>
                </div>
                <div class="spec-cell">
                  <span class="spec-key">RAM / Flash</span>
                  <span class="spec-val">${{d.ram_mb || '?'}}M / ${{d.flash_mb || '?'}}M</span>
                </div>
                <div class="spec-cell">
                  <span class="spec-key">Ethernet</span>
                  <span class="spec-val">${{d.ethernet_1g ? d.ethernet_1g + 'x 1G' : '-'}}</span>
                </div>
                <div class="spec-cell">
                  <span class="spec-key">Cihaz Tipi</span>
                  <span class="spec-val">${{d.devicetype || 'Router'}}</span>
                </div>
              </div>

              <div class="card-badges-row">
                <span class="install-method-badge ${{mInfo.type}}" title="${{mInfo.desc}}">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    ${{mInfo.type === 'success' ? '<polyline points="20 6 9 17 4 12"></polyline>' : 
                      mInfo.type === 'warning' ? '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line>' :
                      mInfo.type === 'danger' ? '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>' :
                      '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline>'}}
                  </svg>
                  <span>${{mInfo.label}}</span>
                </span>

                ${{versionStr ? `
                  <div class="revision-box" title="Bu modelin yalnızca belirtilen donanım revizyonu OpenWrt ile uyumludur. Satın alırken kutu arkasındaki versiyon numarasını kontrol ediniz.">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <span>Revizyon: <b>${{versionStr}}</b></span>
                  </div>
                ` : ''}}
              </div>
            </div>

            <div>
              <div class="card-footer-actions">
                ${{d.epey_url ? `<a href="${{d.epey_url}}" target="_blank" class="btn btn-sm">Epey ↗</a>` : ''}}
                ${{d.akakce_search_url ? `<a href="${{d.akakce_search_url}}" target="_blank" class="btn btn-sm">Akakçe ↗</a>` : ''}}
                <button class="btn btn-sm" onclick="showDetails(${{idx}})">Detaylar</button>
              </div>

              <div class="card-links-row">
                ${{d.device_page ? `<a href="${{d.device_page}}" target="_blank">OpenWrt ToH Sayfası ↗</a>` : '<span>-</span>'}}
                <span style="font-family: var(--font-mono); font-size: 0.6875rem;">#${{idx + 1}}</span>
              </div>
            </div>
          </div>
        `;
      }});
      container.innerHTML = html;
    }}

    function renderTable() {{
      const tbody = document.getElementById('tableBody');
      if (!filteredList.length) {{
        tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding: 3rem; color: var(--text-subtle);">Kriterlere uygun cihaz bulunamadı</td></tr>`;
        return;
      }}

      let html = '';
      filteredList.forEach((d, idx) => {{
        const priceDisplay = d.price && d.price.includes('TL') ? d.price : '-';
        const hasImg = !!d.image_url;
        const imgMarkup = hasImg 
          ? `<img src="${{d.image_url}}" alt="" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">`
          : '';
        const fallbackStyle = hasImg ? 'style="display:none;"' : '';
        const mInfo = getInstallMethodInfo(d);
        const versionStr = formatVersion(d.version) || '-';

        html += `
          <tr>
            <td>
              <div class="table-device-cell">
                <div class="table-thumb">
                  ${{imgMarkup}}
                  <div class="table-thumb-fallback" ${{fallbackStyle}}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="20" height="20">
                      <rect x="2" y="13" width="20" height="8" rx="2"></rect>
                    </svg>
                  </div>
                </div>
                <div>
                  <div style="font-weight: 600; color: var(--text);">${{d.brand}} ${{d.model}}</div>
                  <div style="font-size: 0.75rem; color: var(--text-subtle); max-width: 240px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{d.market_title}}</div>
                </div>
              </div>
            </td>
            <td style="font-family: var(--font-mono); font-weight: 600; white-space: nowrap;">${{priceDisplay}}</td>
            <td>
              <span class="install-method-badge ${{mInfo.type}}" style="font-size: 0.65rem; padding: 0.15rem 0.4rem;" title="${{mInfo.desc}}">
                ${{mInfo.label}}
              </span>
            </td>
            <td style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--revision-text); font-weight: 600; white-space: nowrap;">${{versionStr}}</td>
            <td>${{getReleasePill(d.supported_rel)}}</td>
            <td style="font-family: var(--font-mono); font-size: 0.75rem;">${{d.cpu || '-'}}</td>
            <td style="font-family: var(--font-mono); font-size: 0.75rem;">${{d.ram_mb || '?'}} MB</td>
            <td style="font-family: var(--font-mono); font-size: 0.75rem;">${{d.flash_mb || '?'}} MB</td>
            <td style="white-space: nowrap;">
              <div style="display: flex; gap: 0.35rem;">
                ${{d.epey_url ? `<a href="${{d.epey_url}}" target="_blank" class="btn btn-sm">Epey</a>` : ''}}
                ${{d.akakce_search_url ? `<a href="${{d.akakce_search_url}}" target="_blank" class="btn btn-sm">Akakçe</a>` : ''}}
                <button class="btn btn-sm" onclick="showDetails(${{idx}})">Detay</button>
              </div>
            </td>
          </tr>
        `;
      }});
      tbody.innerHTML = html;
    }}

    function showDetails(idx) {{
      const d = filteredList[idx];
      if (!d) return;

      document.getElementById('modalBrand').innerText = d.brand || 'Cihaz';
      document.getElementById('modalTitle').innerText = `${{d.model || ''}} — ${{d.market_title || ''}}`;

      const photoWrap = document.getElementById('modalPhotoWrap');
      const photoImg = document.getElementById('modalPhoto');
      if (d.image_url) {{
        photoImg.src = d.image_url;
        photoWrap.style.display = 'flex';
      }} else {{
        photoWrap.style.display = 'none';
      }}

      const mInfo = getInstallMethodInfo(d);
      const versionStr = formatVersion(d.version);

      const warningWrap = document.getElementById('modalWarningWrap');
      const warningText = document.getElementById('modalWarningText');
      let warnings = [];
      if (versionStr) {{
        warnings.push(`⚠️ <b>Donanım Revizyonu:</b> Bu cihazın sadece <b>${{versionStr}}</b> revizyonu desteklenmektedir. Satın alırken kutunun altındaki versiyon etiketini teyit ediniz.`);
      }}
      if (mInfo.type === 'warning' || mInfo.type === 'danger') {{
        warnings.push(`⚡ <b>Kurulum Yöntemi:</b> ${{mInfo.label}} — ${{mInfo.desc}}`);
      }}
      if (warnings.length > 0) {{
        warningText.innerHTML = warnings.join('<br><br>');
        warningWrap.style.display = 'block';
      }} else {{
        warningWrap.style.display = 'none';
      }}

      const details = [
        ['Pazar Fiyatı', d.price || 'Fiyat Belirtilmemiş'],
        ['Kurulum Yöntemi', mInfo.label],
        ['Donanım Revizyonu', versionStr || 'Tüm Revizyonlar'],
        ['OpenWrt Sürümü', d.supported_rel || '-'],
        ['İşlemci (SoC)', d.cpu || '-'],
        ['Hedef Mimari', d.target || '-'],
        ['RAM Boyutu', `${{d.ram_mb || '-'}} MB`],
        ['Flash Boyutu', `${{d.flash_mb || '-'}} MB`],
        ['Paket Mimarisi', d.packagearchitecture || '-'],
        ['Cihaz Tipi', d.devicetype || d.category || 'Router'],
        ['1G Ethernet', d.ethernet_1g || '-'],
        ['2.5G Ethernet', d.ethernet_2_5g || '-'],
        ['Wi-Fi 2.4 GHz', d.wlan24ghz || '-'],
        ['Wi-Fi 5.0 GHz', d.wlan50ghz || '-'],
        ['USB Portları', Array.isArray(d.usbports) ? d.usbports.join(', ') : (d.usbports || '-')],
        ['Bootloader', d.bootloader || '-']
      ];

      let gridHtml = '';
      details.forEach(([lbl, val]) => {{
        gridHtml += `
          <div class="modal-field">
            <span class="modal-key">${{lbl}}</span>
            <span class="modal-val">${{val}}</span>
          </div>
        `;
      }});
      document.getElementById('modalDetails').innerHTML = gridHtml;

      document.getElementById('modalComments').innerText = d.comments || 'Bu cihaz için özel bir uyarı bulunmuyor. Cihaz kurulum adımları ve firmware dosyaları için aşağıdaki OpenWrt bağlantısını kullanabilirsiniz.';

      let linksHtml = '';
      if (d.epey_url) linksHtml += `<a href="${{d.epey_url}}" target="_blank" class="btn btn-sm">Epey Ürün Sayfası ↗</a>`;
      if (d.akakce_search_url) linksHtml += `<a href="${{d.akakce_search_url}}" target="_blank" class="btn btn-sm">Akakçe Fiyatları ↗</a>`;
      if (d.device_page) linksHtml += `<a href="${{d.device_page}}" target="_blank" class="btn btn-primary btn-sm">OpenWrt Resmi ToH ↗</a>`;
      
      const issueTitle = encodeURIComponent(`[Hatalı Eşleşme / Sorun]: ${{d.brand || ''}} ${{d.model || ''}}`);
      const issueUrl = `https://github.com/m24ih/openwrt-turkiye/issues/new?template=router_mismatch.yml&title=${{issueTitle}}`;
      linksHtml += `<a href="${{issueUrl}}" target="_blank" class="btn btn-sm" style="background: var(--warning-subtle); border-color: var(--warning-border); color: var(--warning);" title="Hatalı eşleşme veya donanım sorunu bildir">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: -1px; margin-right: 4px;">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        Sorun Bildir ↗
      </a>`;

      document.getElementById('modalLinks').innerHTML = linksHtml;
      document.getElementById('detailModal').showModal();
    }}

    function closeModal() {{
      document.getElementById('detailModal').close();
    }}

    document.getElementById('detailModal').addEventListener('click', (e) => {{
      const dialog = document.getElementById('detailModal');
      const rect = dialog.getBoundingClientRect();
      const inDialog = (rect.top <= e.clientY && e.clientY <= rect.top + rect.height && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
      if (!inDialog) {{
        dialog.close();
      }}
    }});

    init();
  </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    shutil.copyfile(OUTPUT_HTML, WEB_HTML)
    for fname in ["favicon.svg", "favicon.ico", "apple-touch-icon.png"]:
        src_file = PROJECT_ROOT / fname
        if src_file.exists():
            shutil.copyfile(src_file, WEB_DIR / fname)
    print(f"[Generator] Successfully generated web dashboard at {OUTPUT_HTML} and {WEB_HTML}")
    return OUTPUT_HTML
