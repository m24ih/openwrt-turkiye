#!/usr/bin/env bash
# OpenWrt Türkiye - Yerel Haftalık Cron Kurulum Betiği

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(which python3)"
LOG_FILE="$PROJECT_DIR/data/update_cron.log"

CRON_CMD="0 4 * * 1 cd $PROJECT_DIR && $PYTHON_BIN main.py update >> $LOG_FILE 2>&1"

# Mevcut crontab'ı al, eğer bu komut yoksa ekle
(crontab -l 2>/dev/null | grep -v "openwrt-turkiye/main.py" ; echo "$CRON_CMD") | crontab -

echo "✅ Haftalık yerel cron görevi başarıyla kuruldu!"
echo "   Zaman: Her Pazartesi saat 04:00"
echo "   Komut: cd $PROJECT_DIR && $PYTHON_BIN main.py update"
echo "   Log Dosyası: $LOG_FILE"
