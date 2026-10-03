#!/usr/bin/env python3
"""
OpenWrt Türkiye - Ağ Cihazları Kataloğu & Fiyat Takipçisi
CLI Yönetim Aracı
"""

import argparse
import sys
import json
import http.server
import socketserver
from pathlib import Path

from src.config import PROJECT_ROOT, OUTPUT_FILTERED_JSON, OUTPUT_HTML
from src.openwrt import fetch_latest_toh, load_local_toh
from src.crawlers import crawl_epey, crawl_akakce
from src.matcher import match_and_enrich
from src.generator import generate_html

def cmd_update(args):
    """Haftalık tam güncelleme: OpenWrt ToH + Pazar Crawl + Eşleştirme + Site Üretimi"""
    print("=" * 60)
    print("🚀 OpenWrt Türkiye Tam Güncelleme Başlatılıyor...")
    print("=" * 60)
    
    # 1. OpenWrt ToH Güncelleme
    owrt_items, has_toh_changes, new_devices = fetch_latest_toh()
    
    # 2. Pazar Fiyatları ve Modellerini Çekme (Epey + Akakçe)
    print("\n📦 Türkiye pazarındaki güncel ağ ürünleri taranıyor...")
    epey_items = crawl_epey()
    akakce_items = crawl_akakce()
    
    all_market = epey_items + akakce_items
    print(f"\n[Market] Toplam {len(all_market)} pazar kaydı toplandı.")
    
    # 3. Akıllı Eşleştirme & Zenginleştirme
    matched = match_and_enrich(all_market, owrt_items)
    
    # 4. Web Arayüzünü Yeniden Derleme
    generate_html(matched)
    
    print("\n" + "=" * 60)
    print(f"✅ Güncelleme tamamlandı!")
    print(f"   - OpenWrt ToH: {len(owrt_items)} cihaz (+{new_devices} yeni)")
    print(f"   - Türkiye Pazar Ürünleri: {len(all_market)} kayıt")
    print(f"   - Türkiye'de Satışta Olan OpenWrt Cihazları: {len(matched)} model")
    print(f"   - Web Dashboard: {OUTPUT_HTML}")
    print("=" * 60)

def cmd_update_openwrt(args):
    """Sadece resmi OpenWrt Table of Hardware veritabanını günceller"""
    items, has_changes, count = fetch_latest_toh()
    print(f"OpenWrt ToH güncellendi: {len(items)} cihaz (+{count} yeni).")

def cmd_update_prices(args):
    """Sadece pazar fiyatlarını günceller ve mevcut ToH ile eşleştirir"""
    owrt_items = load_local_toh()
    if not owrt_items:
        owrt_items, _, _ = fetch_latest_toh()
        
    print("Türkiye pazarı taranıyor...")
    epey_items = crawl_epey()
    akakce_items = crawl_akakce()
    all_market = epey_items + akakce_items
    
    matched = match_and_enrich(all_market, owrt_items)
    generate_html(matched)
    print(f"Fiyatlar ve eşleşen {len(matched)} model güncellendi.")

def cmd_build(args):
    """Mevcut verilerden web sitesini derler"""
    out = generate_html()
    print(f"Web arayüzü başarıyla üretildi: {out}")

def cmd_search(args):
    """Terminal üzerinden OpenWrt destekli cihaz ve fiyat sorgulama"""
    if not OUTPUT_FILTERED_JSON.exists():
        print(f"Hata: {OUTPUT_FILTERED_JSON} bulunamadı. Önce `python main.py update` çalıştırın.")
        return
        
    with open(OUTPUT_FILTERED_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    query = args.query.lower().strip()
    results = []
    for d in data:
        haystack = f"{d.get('brand')} {d.get('model')} {d.get('market_title')} {d.get('cpu')} {d.get('target')}".lower()
        if query in haystack:
            results.append(d)
            
    print(f"\n🔍 '{args.query}' için bulunan {len(results)} cihaz:\n")
    for r in results:
        price = r.get('price') or 'Fiyat Yok'
        rel = r.get('supported_rel') or '-'
        cpu = r.get('cpu') or '-'
        ram = r.get('ram_mb') or '?'
        flash = r.get('flash_mb') or '?'
        print(f" • [{r.get('brand')}] {r.get('model')} ({price})")
        print(f"   Piyasa Adı: {r.get('market_title')}")
        print(f"   Donanım: CPU: {cpu} | RAM: {ram}MB | Flash: {flash}MB | OpenWrt: v{rel}")
        print(f"   Epey: {r.get('epey_url') or '-'}")
        print(f"   Akakçe: {r.get('akakce_search_url') or '-'}")
        print()

def cmd_serve(args):
    """Web arayüzünü yerel bir HTTP sunucusunda başlatır"""
    port = args.port
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(PROJECT_ROOT), **k)
            
    print(f"🌍 OpenWrt Türkiye yerel sunucusu başlatıldı: http://localhost:{port}")
    print("Durdurmak için Ctrl+C tuşlarına basın.")
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatıldı.")

def main():
    parser = argparse.ArgumentParser(
        description="OpenWrt Türkiye - Ağ Cihazları Kataloğu ve Fiyat Takipçisi CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Komutlar")
    
    # update
    subparsers.add_parser("update", help="Tam haftalık güncelleme (ToH + Fiyatlar + Site)")
    
    # update-openwrt
    subparsers.add_parser("update-openwrt", help="Yalnızca OpenWrt ToH veritabanını günceller")
    
    # update-prices
    subparsers.add_parser("update-prices", help="Yalnızca pazar fiyatlarını günceller")
    
    # build
    subparsers.add_parser("build", help="Mevcut verilerden web sitesini yeniden üretir")
    
    # search
    search_p = subparsers.add_parser("search", help="Cihaz ve fiyat sorgula")
    search_p.add_argument("query", type=str, help="Aranacak marka, model veya işlemci")
    
    # serve
    serve_p = subparsers.add_parser("serve", help="Yerel web sunucusunu başlat")
    serve_p.add_argument("--port", type=int, default=8080, help="Port numarası (varsayılan: 8080)")
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    commands = {
        "update": cmd_update,
        "update-openwrt": cmd_update_openwrt,
        "update-prices": cmd_update_prices,
        "build": cmd_build,
        "search": cmd_search,
        "serve": cmd_serve
    }
    
    commands[args.command](args)

if __name__ == "__main__":
    main()
