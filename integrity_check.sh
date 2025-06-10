#!/bin/bash

# Klasör ve dosya yolları
TARGET_DIR="/opt/scripts"
BASELINE_FILE="/opt/scripts/baseline_hashes.txt"
REPORT_FILE="/opt/scripts/integrity_report.txt"
TEMP_FILE="/opt/scripts/current_hashes.txt"

# Şimdiki durumu al
find "$TARGET_DIR" -type f -exec sha256sum {} \; 2>/dev/null | sort > "$TEMP_FILE"

# Eğer baseline yoksa, oluştur ve çık
if [ ! -f "$BASELINE_FILE" ]; then
    cp "$TEMP_FILE" "$BASELINE_FILE"
    exit 0
fi

# Farkları bul
DIFF=$(diff "$BASELINE_FILE" "$TEMP_FILE")

# Eğer fark varsa, rapor oluştur
if [ -n "$DIFF" ]; then
    {
        echo "=== Integrity Check Report: $(date) ==="
        echo ""
        echo "$DIFF" | grep -E '^[<>]' | while read -r line; do
            if [[ $line == \<* ]]; then
                echo "Silinmiş veya değiştirilmiş: ${line:2}"
            elif [[ $line == \>* ]]; then
                echo "Yeni veya değiştirilmiş: ${line:2}"
            fi
        done
        echo ""
    } >> "$REPORT_FILE"
fi

# Temizle
rm -f "$TEMP_FILE"
