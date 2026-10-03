# 🌐 OpenWrt Türkiye - Ağ Cihazları Kataloğu & Fiyat Takipçisi

[![OpenWrt Version](https://img.shields.io/badge/OpenWrt-v25%20%7C%20v24-00a6e0?style=flat-square&logo=openwrt)](https://openwrt.org)
[![Weekly Update](https://img.shields.io/badge/Update-Weekly%20Automated-10b981?style=flat-square&logo=githubactions)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

Türkiye e-ticaret piyasasında (**Epey** ve **Akakçe**) aktif olarak satışta olan, resmi **OpenWrt** destekli router, modem, menzil genişletici ve yönetilebilir switch'lerin **otomatik olarak takip edildiği, teknik özellikleriyle zenginleştirildiği ve güncel fiyatlarıyla listelendiği** açık kaynaklı bir katalog ve otomasyon platformudur.

---

## ✨ Özellikler

* 🔄 **Haftalık Otomatik Senkronizasyon:**
  * Her hafta resmi OpenWrt Table of Hardware (`toh.openwrt.org`) veritabanını tarar.
  * Yeni eklenen cihaz veya donanım revizyonlarını tespit eder.
  * Model Türkiye piyasasında (Epey/Akakçe) satışa çıkmışsa otomatik olarak kataloğa ekler ve fiyatını takip eder.
* 📊 **Zenginleştirilmiş Donanım Özellikleri:**
  * İşlemci (CPU/SoC), RAM, Flash boyutu, Wi-Fi nesli (Wi-Fi 6 AX / Wi-Fi 5 AC), Ethernet portları (1G / 2.5G), hedef mimari ve **doğrudan resmi firmware indirme bağlantıları**.
* 🔍 **Anlık Canlı Filtreleme & Arama:**
  * Marka rozetleri (TP-Link, ASUS, Cudy, Xiaomi, MikroTik, Ubiquiti vb.).
  * Wi-Fi nesli, minimum RAM/Flash gereksinimi ve OpenWrt kararlı sürüm filtreleri.
* 🌓 **Modern Web Dashboard:**
  * Kart (Grid) ve Tablo (Dense Table) görünümü.
  * Karanlık ve aydınlık tema desteği.
  * Sonuçları tek tıkla **JSON** veya **CSV (Excel)** olarak dışa aktarma.
* ⚡ **Sıfır Sunucu Maliyeti (GitHub Actions + Pages):**
  * Dahili CI/CD boru hattı sayesinde hiçbir sunucu kiralamadan tamamen GitHub altyapısında çalışır ve web arayüzünü güncel tutar.

---

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler & Kurulum

Python 3.10+ gereklidir:

```bash
git clone https://github.com/melih/openwrt-turkiye.git
cd openwrt-turkiye

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Kullanım (CLI Komutları)

`main.py` yönetim aracı ile tüm işlemleri terminalden yürütebilirsiniz:

```bash
# 1. Tam haftalık güncellemeyi başlat (ToH çek + Pazar fiyatlarını tara + Eşleştir + Siteyi derle)
python main.py update

# 2. Terminalden hızlı cihaz / fiyat sorgula
python main.py search "wr3000"
python main.py search "ax3000t"
python main.py search "mt7621"

# 3. Yalnızca OpenWrt resmi veritabanını güncelle
python main.py update-openwrt

# 4. Yalnızca pazar fiyatlarını tara ve eşleştir
python main.py update-prices

# 5. Mevcut veriden web sitesini yeniden üret
python main.py build

# 6. Web arayüzünü yerel sunucuda başlat (http://localhost:8080)
python main.py serve --port 8080
```

---

## 🤖 Haftalık Otomasyon Kurulumu

### Seçenek A: GitHub Actions & GitHub Pages (Önerilen)

Projeyi GitHub deponuza yüklediğinizde hazır gelen `.github/workflows/weekly_update.yml` iş akışı devreye girer:
1. **Her Pazartesi saat 03:00 UTC'de** otomatik olarak çalışır.
2. OpenWrt ToH ve Epey/Akakçe pazarını tarar.
3. Değişiklik varsa repoya otomatik commit atar (`chore(data): weekly update...`).
4. Güncellenen `index.html` sayfasını anında **GitHub Pages** üzerinde canlıya alır.

> **GitHub Pages'ı Etkinleştirmek İçin:**
> Repo sayfanızda **Settings > Pages > Build and deployment > Source** seçeneğini **GitHub Actions** olarak ayarlamanız yeterlidir.

### Seçenek B: Yerel Cron ile Güncelleme (Linux / VDS)

GitHub Actions yerine kendi bilgisayarınızda veya sunucunuzda haftalık çalıştırmak için:

```bash
./scripts/setup_cron.sh
```

Bu betik, her Pazartesi saat 04:00'te güncelleme komutunu çalıştıracak cron görevini otomatik olarak tanımlar ve loglarını `data/update_cron.log` altına yazar.

---

## 📂 Proje Mimarisi

```
openwrt-turkiye/
├── data/
│   ├── raw/
│   │   ├── openwrt_toh_all.json    # Upstream OpenWrt resmi ToH verisi
│   │   └── market_products.json    # Pazar ham ürün dump'ı
│   └── openwrt_turkiye.json        # Zenginleştirilmiş ana katalog verisi
├── src/
│   ├── crawlers/
│   │   ├── epey.py                 # Epey crawler motoru (curl_cffi)
│   │   └── akakce.py               # Akakçe crawler motoru (curl_cffi)
│   ├── config.py                   # Merkezi yapılandırma ve yollar
│   ├── openwrt.py                  # Resmi ToH çekici & versiyon karşılaştırıcı
│   ├── matcher.py                  # Token ve donanım revizyonu eşleştirici
│   └── generator.py                # Modern HTML/JS web dashboard üreticisi
├── web/
│   └── index.html                  # Web arayüzü kopyası
├── scripts/
│   └── setup_cron.sh               # Yerel cron kurulum betiği
├── .github/workflows/
│   └── weekly_update.yml           # GitHub Actions haftalık otomasyonu
├── index.html                      # Canlı bağımsız web uygulaması
├── main.py                         # Ana CLI yönetim arayüzü
├── requirements.txt
└── README.md
```

---

## 🛡️ Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında sunulmaktadır.
