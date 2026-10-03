# 🌐 OpenWrt Türkiye — Ağ Cihazları Kataloğu & Fiyat Takipçisi

[![Canlı Site](https://img.shields.io/badge/Canlı%20Site-openwrt.melihak.me-6366f1?style=flat-square&logo=cloudflare)](https://openwrt.melihak.me)
[![OpenWrt Version](https://img.shields.io/badge/OpenWrt-v25%20%7C%20v24-00a6e0?style=flat-square&logo=openwrt)](https://openwrt.org)
[![Weekly Update](https://img.shields.io/badge/Update-Weekly%20Automated-10b981?style=flat-square&logo=githubactions)](https://github.com/m24ih/openwrt-turkiye/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

Türkiye e-ticaret piyasasında (**Epey** ve **Akakçe**) aktif olarak satışta olan, resmi **OpenWrt** destekli router, modem, menzil genişletici ve ağ donanımlarının **otomatik olarak takip edildiği, donanım revizyon uyarıları ve kurulum yöntemleriyle zenginleştirildiği, güncel piyasa fiyatlarıyla listelendiği** açık kaynaklı bir katalog ve otomasyon platformudur.

🔗 **Canlı Web Kataloğu:** [https://openwrt.melihak.me](https://openwrt.melihak.me)

---

## ✨ Öne Çıkan Özellikler

* 🔄 **Haftalık Otomatik Senkronizasyon (GitHub Actions):**
  * Her hafta resmi OpenWrt Table of Hardware (`toh.openwrt.org`) veritabanını tarar.
  * Yeni eklenen cihaz veya donanım revizyonlarını tespit eder.
  * Model Türkiye piyasasında (Epey / Akakçe) satışa çıkmışsa otomatik olarak kataloğa ekler ve fiyatını takip eder.
* ⚠️ **Kritik Donanım Revizyon Uyarıları:**
  * Türkiye pazarında sıkça yaşanan revizyon uyuşmazlıkları (örn: TP-Link modellerinde piyasadaki yeni revizyonun kilitli olması veya Xiaomi'nin spesifik anakart kodları) kartların üzerinde belirgin turuncu uyarı şeritleriyle (`⚠️ Revizyon Uyarısı`) gösterilir.
* 🛠️ **OpenWrt Kurulum Yöntemi Tespiti & Filtresi:**
  * Cihazlar kurulum zorluğuna göre sınıflandırılır:
    * 🟢 **Kolay Web Arayüzü** *(Cudy, GL.iNet vb. doğrudan web panelinden dosya yükleme)*
    * 🟡 **Yazılım Açığı (Exploit / SSH)** *(Xiaomi Mi 4A Gigabit OpenWRTInvasion / XMir-patcher vb.)*
    * 🔵 **TFTP / Ağ Kurtarma** *(TP-Link, Asus, Ubiquiti kurtarma modları)*
    * 🔴 **Seri Port (UART / Lehim)** *(Donanıma doğrudan seri konsol müdahalesi)*
  * Filtre panelinden tek tıkla yalnızca kolay kurulan veya exploit gerektirmeyen modeller ayrıştırılabilir.
* 🖼️ **Ürün Fotoğrafları:**
  * Epey ve Akakçe üzerinden çekilen yüksek çözünürlüklü ürün görselleri hem kart görünümünde hem de kompakt tablo görünümünde listelenir.
* 💰 **Gelişmiş Fiyat & Donanım Sıralaması:**
  * Fiyatı listelenmeyen ürünler tüm sıralama modlarında (artan/azalan fiyat, A-Z, RAM, çıkış yılı) daima listenin en altına toplanır.
* 🔀 **Topluluk Geri Bildirimi & GitHub Issue Şablonları:**
  * Cihaz modalındaki **"Sorun Bildir"** butonu, ilgili cihazın modelini otomatik doldurarak `Hatalı Eşleşen Router (Router Mismatch)` şablonuna yönlendirir.
  * Üst menüdeki buton ise eksik cihaz ekleme, hatalı teknik bilgi düzeltme ve hata bildirimleri için yapılandırılmış GitHub Issue formlarını açar.
* 🎨 **Modern & Minimalist Mühendislik Estetiği (Anti-AI-Slop):**
  * Linear / Vercel / Raycast arayüz standartlarına uygun koyu/açık tema, hairline kenarlıklar, Inter ve JetBrains Mono tipografisi, çok katmanlı vektörel Favicon seti (`favicon.svg`, `favicon.ico`, `apple-touch-icon.png`).
  * Sonuçları tek tıkla **JSON** veya **CSV (Excel)** olarak dışa aktarma ve klavye kısayoluyla (`/`) anında arama.

---

## 🚀 Hızlı Başlangıç

### 1. Depoyu Klonlama & Kurulum

Python 3.10+ gereklidir:

```bash
git clone https://github.com/m24ih/openwrt-turkiye.git
cd openwrt-turkiye

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Yönetim Aracı (CLI Komutları)

`main.py` CLI aracı ile tüm işlemleri terminalden yürütebilirsiniz:

```bash
# 1. Tam haftalık güncellemeyi başlat (ToH çek + Pazar fiyatlarını tara + Eşleştir + Siteyi derle)
python main.py update

# 2. Terminalden hızlı cihaz / donanım / fiyat sorgula
python main.py search "wr3000"
python main.py search "ax3000t"
python main.py search "mt7621"

# 3. Yalnızca OpenWrt resmi Table of Hardware veritabanını güncelle
python main.py update-openwrt

# 4. Yalnızca pazar fiyatlarını tara ve eşleştir
python main.py update-prices

# 5. Mevcut veriden web sitesini yeniden derle
python main.py build

# 6. Web arayüzünü yerel geliştirme sunucusunda başlat (http://localhost:8080)
python main.py serve --port 8080
```

---

## 🤖 Otomasyon & Canlı Yayın Mimarisi

### GitHub Actions & GitHub Pages (Varsayılan)

Depoda bulunan `.github/workflows/` iş akışları ile süreç tamamen otomatiktir:
1. **Haftalık Senkronizasyon (`weekly_update.yml`):**
   * Her Pazartesi saat 03:00 UTC'de çalışır.
   * OpenWrt ToH ve Türkiye pazarını (Epey / Akakçe) tarar, eşleştirir ve `openwrt_turkiye.json` dosyasını günceller.
   * Cloudflare veya bot koruması durumunda mevcut önbelleği koruyan akıllı eşik korumasına sahiptir.
2. **Statik Dağıtım (`deploy.yml`):**
   * `main` branch'ine yapılan her commit sonrasında `index.html` ve statik varlıkları derleyip **[openwrt.melihak.me](https://openwrt.melihak.me)** özel alan adına anında canlıya alır.

### Yerel Cron ile Güncelleme (Alternatif Linux Sunucu / VDS)

GitHub Actions yerine kendi sunucunuzda çalıştırmak isterseniz:

```bash
chmod +x ./scripts/setup_cron.sh
./scripts/setup_cron.sh
```

---

## 📂 Proje Dizin Yapısı

```
openwrt-turkiye/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── router_mismatch.yml     # Hatalı eşleşen cihaz bildirim formu
│   │   ├── missing_device.yml      # Pazardaki eksik OpenWrt cihaz formu
│   │   ├── incorrect_info.yml      # Donanım / revizyon / kurulum düzeltme formu
│   │   ├── bug_report.yml          # Web arayüzü hata bildirim formu
│   │   ├── feature_request.yml     # Yeni özellik ve öneri formu
│   │   └── config.yml              # Issue şablon menüsü ve faydalı linkler
│   └── workflows/
│       ├── deploy.yml              # GitHub Pages otomatik yayınlama
│       └── weekly_update.yml       # Haftalık zamanlanmış pazar güncellemesi
├── data/
│   ├── raw/
│   │   ├── openwrt_toh_all.json    # Upstream OpenWrt resmi ToH verisi
│   │   └── market_products.json    # Epey ve Akakçe ham pazar ürün dump'ı
│   └── openwrt_turkiye.json        # Zenginleştirilmiş ana katalog verisi
├── src/
│   ├── crawlers/
│   │   ├── epey.py                 # Epey crawler motoru (curl_cffi / impersonate)
│   │   └── akakce.py               # Akakçe crawler motoru (curl_cffi / impersonate)
│   ├── config.py                   # Merkezi yapılandırma ve dosya yolları
│   ├── openwrt.py                  # Resmi ToH çekici & versiyon karşılaştırıcı
│   ├── matcher.py                  # Token ve donanım revizyonu eşleştirici
│   └── generator.py                # Modern HTML/JS web dashboard üreticisi
├── web/                            # Statik web dağıtım paketi
├── scripts/
│   └── setup_cron.sh               # Yerel Linux cron kurulum betiği
├── favicon.svg                     # Çok katmanlı vektörel OpenWrt squircle favicon
├── favicon.ico                     # Multi-res (16x16, 32x32, 48x48) favicon
├── apple-touch-icon.png            # 180x180 Apple Touch Icon
├── CNAME                           # openwrt.melihak.me alan adı yönlendirmesi
├── index.html                      # Bağımsız tek sayfa web uygulaması (Single-File)
├── main.py                         # Ana CLI yönetim konsolu
├── requirements.txt                # Python bağımlılıkları
└── README.md                       # Proje dokümantasyonu
```

---

## 🤝 Katkıda Bulunma & Topluluk

* Türkiye pazarında satışta olan fakat katalogda yer almayan bir model biliyorsanız veya bir cihazın donanım revizyonu/kurulum bilgisi hatalıysa [GitHub Issues](https://github.com/m24ih/openwrt-turkiye/issues/new/choose) üzerinden bildirebilirsiniz.
* Pull Request'ler memnuniyetle kabul edilir. Lütfen değişiklik yapmadan önce `python main.py build` komutu ile çıktıyı doğrulayınız.

---

## 🛡️ Lisans

Bu proje [MIT Lisansı](LICENSE) altında geliştirilmektedir. OpenWrt, OpenWrt projesinin tescilli ticari markasıdır.
