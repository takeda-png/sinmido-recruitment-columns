#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終修復スクリプト：
1. Canva iframe を削除
2. スライダー画像を追加
3. 各セクション下に画像を追加
"""
import sys
import io
import re
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = Path("C:/Users/taked/frontend-pomodoro")

COLUMNS = {
    "02-regional-hiring.html": {
        "slider_images": ["g5.jpg", "g6.jpg", "g7.jpg", "g8.jpg"],
        "section_replacements": [
            # Canva iframe → 画像に置換
            (r'<iframe src="https://www\.canva\.com/design/DAHCHX1mu9s/embed"[^>]*></iframe>',
             '<img src="slider-images/g5.jpg" alt="地域創生採用戦略" class="section-image">\n            <div class="image-caption">地域創生採用戦略</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHfVUDtw/embed"[^>]*></iframe>',
             '<img src="slider-images/g6.jpg" alt="地方企業の人材獲得" class="section-image">\n            <div class="image-caption">地方企業の人材獲得</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHQ2qwZM/embed"[^>]*></iframe>',
             '<img src="slider-images/g7.jpg" alt="Uターン・Iターン人材" class="section-image">\n            <div class="image-caption">Uターン・Iターン人材</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHSY65n0/embed"[^>]*></iframe>',
             '<img src="slider-images/g8.jpg" alt="地域とのつながり" class="section-image">\n            <div class="image-caption">地域とのつながり</div>'),
        ]
    },
    "03-new-employee-retention.html": {
        "slider_images": ["g9.jpg", "g10.jpg", "g11.jpg", "g12.jpg"],
        "section_replacements": [
            (r'<iframe src="https://www\.canva\.com/design/DAHCHWu7PPY/embed"[^>]*></iframe>',
             '<img src="slider-images/g9.jpg" alt="新入社員離職原因" class="section-image">\n            <div class="image-caption">新入社員離職原因</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHUgXhi8/embed"[^>]*></iframe>',
             '<img src="slider-images/g10.jpg" alt="オンボーディング" class="section-image">\n            <div class="image-caption">オンボーディング</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHfqFduE/embed"[^>]*></iframe>',
             '<img src="slider-images/g11.jpg" alt="メンター制度" class="section-image">\n            <div class="image-caption">メンター制度</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHSfeWio/embed"[^>]*></iframe>',
             '<img src="slider-images/g12.jpg" alt="長期定着施策" class="section-image">\n            <div class="image-caption">長期定着施策</div>'),
        ]
    },
    "04-midcareer-hiring.html": {
        "slider_images": ["g13.jpg", "g14.jpg", "g15.jpg", "g16.jpg"],
        "section_replacements": [
            (r'<iframe src="https://www\.canva\.com/design/DAHCHdW6ZIg/embed"[^>]*></iframe>',
             '<img src="slider-images/g13.jpg" alt="中途採用失敗分析" class="section-image">\n            <div class="image-caption">中途採用失敗分析</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHV1sbtw/embed"[^>]*></iframe>',
             '<img src="slider-images/g14.jpg" alt="ターゲット人材定義" class="section-image">\n            <div class="image-caption">ターゲット人材定義</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHg2Hpvk/embed"[^>]*></iframe>',
             '<img src="slider-images/g15.jpg" alt="ジョブディスクリプション" class="section-image">\n            <div class="image-caption">ジョブディスクリプション</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHfR1rJE/embed"[^>]*></iframe>',
             '<img src="slider-images/g16.jpg" alt="オンボーディングと活躍" class="section-image">\n            <div class="image-caption">オンボーディングと活躍</div>'),
        ]
    },
    "05-recruitment-branding.html": {
        "slider_images": ["g17.jpg", "g18.jpg", "g19.jpg", "g20.jpg"],
        "section_replacements": [
            (r'<iframe src="https://www\.canva\.com/design/DAHCHb5gwtw/embed"[^>]*></iframe>',
             '<img src="slider-images/g17.jpg" alt="ブランド概要" class="section-image">\n            <div class="image-caption">ブランド概要</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHYeKJmU/embed"[^>]*></iframe>',
             '<img src="slider-images/g18.jpg" alt="企業文化発信" class="section-image">\n            <div class="image-caption">企業文化発信</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHQRvtKk/embed"[^>]*></iframe>',
             '<img src="slider-images/g19.jpg" alt="社員の声" class="section-image">\n            <div class="image-caption">社員の声</div>'),
            (r'<iframe src="https://www\.canva\.com/design/DAHCHW5NM5o/embed"[^>]*></iframe>',
             '<img src="slider-images/g20.jpg" alt="成果測定" class="section-image">\n            <div class="image-caption">成果測定</div>'),
        ]
    }
}

def fix_column(filepath, slider_images, replacements):
    """コラムを修復"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # スライダー画像のURLを置換
    picsum_pattern = r'src="https://picsum\.photos/\d+/\d+\?random=\d+"'
    slider_srcs = re.findall(picsum_pattern, html)

    for i, img_file in enumerate(slider_images):
        # i 番目の picsum URL を置換
        if i < len(slider_srcs):
            html = html.replace(slider_srcs[i], f'src="slider-images/{img_file}"', 1)

    # Canva iframe を画像に置換
    for pattern, replacement in replacements:
        html = re.sub(pattern, replacement, html, flags=re.IGNORECASE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Fixed: {filepath.name}")

# 修復実行
print("=" * 60)
print("Final fix: Replace Canva iframes with local images")
print("=" * 60)

for filename, config in COLUMNS.items():
    filepath = SCRIPT_DIR / filename
    if filepath.exists():
        fix_column(filepath, config["slider_images"], config["section_replacements"])
    else:
        print(f"✗ File not found: {filename}")

print("\n" + "=" * 60)
print("✓ All columns fixed!")
print("=" * 60)
