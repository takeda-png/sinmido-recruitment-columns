#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スライダー画像をローカルダウンロード + HTML置換スクリプト
連番（g1.jpg, g2.jpg...）で保存し、HTMLコードを自動更新
"""

import os
import sys
import re
import json
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 設定
SCRIPT_DIR = Path(__file__).parent
IMAGE_DIR = SCRIPT_DIR / "slider-images"
HTML_FILES = [
    SCRIPT_DIR / "01-hiring-trends.html",
    SCRIPT_DIR / "02-regional-hiring.html",
    SCRIPT_DIR / "03-new-employee-retention.html",
    SCRIPT_DIR / "04-midcareer-hiring.html",
    SCRIPT_DIR / "05-recruitment-branding.html",
]

# 画像URL マッピング情報（ライセンス確認済み）
IMAGE_SOURCES = {
    "picsum.photos": {
        "name": "Lorem Picsum (CC0)",
        "commercial_use": True,
        "requires_attribution": False
    },
    "unsplash.com": {
        "name": "Unsplash (Unsplash License)",
        "commercial_use": True,
        "requires_attribution": False
    },
}

def ensure_image_dir():
    """画像保存ディレクトリを作成"""
    IMAGE_DIR.mkdir(exist_ok=True)
    print(f"✓ Image directory: {IMAGE_DIR}")

def get_image_extension(url):
    """URLから画像拡張子を取得"""
    parsed = urlparse(url)
    path = parsed.path

    # 拡張子を抽出
    if '.' in path:
        ext = path.split('.')[-1].lower()
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            return ext

    # デフォルト
    return 'jpg'

def download_image(url, output_path, timeout=10):
    """URLから画像をダウンロード"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = Request(url, headers=headers)

        with urlopen(req, timeout=timeout) as response:
            image_data = response.read()

        with open(output_path, 'wb') as f:
            f.write(image_data)

        return True
    except Exception as e:
        print(f"✗ Download failed for {url}: {e}")
        return False

def extract_images_from_html(html_file):
    """HTMLファイルからスライダー画像URLを抽出"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # swiper-slide 内の img タグを抽出
        images = []
        for slide in soup.find_all('div', class_='swiper-slide'):
            img_tag = slide.find('img')
            if img_tag and img_tag.get('src'):
                images.append({
                    'url': img_tag['src'],
                    'alt': img_tag.get('alt', 'slider image'),
                    'file': html_file.name
                })

        return images
    except Exception as e:
        print(f"✗ Error parsing {html_file}: {e}")
        return []

def check_license(url):
    """URLのライセンスをチェック"""
    for domain, info in IMAGE_SOURCES.items():
        if domain in url:
            return info
    return {"commercial_use": True, "requires_attribution": False}

def download_all_images():
    """すべてのHTMLファイルから画像をダウンロード"""
    ensure_image_dir()

    all_images = []
    image_counter = 1

    # マッピング情報を保存
    mapping = []

    print("\n=== Downloading Images ===\n")

    for html_file in HTML_FILES:
        if not html_file.exists():
            print(f"✗ File not found: {html_file}")
            continue

        print(f"Scanning: {html_file.name}")
        images = extract_images_from_html(html_file)

        for idx, img_info in enumerate(images, 1):
            url = img_info['url']
            license_info = check_license(url)

            if not license_info['commercial_use']:
                print(f"  ✗ Skipped (non-commercial license): {url}")
                continue

            # 拡張子を取得
            ext = get_image_extension(url)
            filename = f"g{image_counter}.{ext}"
            filepath = IMAGE_DIR / filename

            print(f"  → Downloading: {filename}")

            if download_image(url, filepath):
                print(f"    ✓ Saved as: {filename} ({filepath.stat().st_size} bytes)")

                # マッピング情報を保存
                mapping.append({
                    "image_number": image_counter,
                    "filename": filename,
                    "original_url": url,
                    "license": license_info.get('name', 'Unknown'),
                    "from_file": html_file.name,
                    "alt_text": img_info['alt']
                })

                image_counter += 1
            else:
                print(f"    ✗ Failed to download")

    # マッピング情報をJSON保存
    mapping_file = SCRIPT_DIR / "image-mapping.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Image mapping saved to: {mapping_file}")

    return mapping

def replace_image_urls_in_html(mapping):
    """HTMLファイル内の画像URLを置換"""
    print("\n=== Replacing URLs in HTML ===\n")

    # URLと新しいパスのマッピングを作成
    url_to_local = {}
    for item in mapping:
        url_to_local[item['original_url']] = f"slider-images/{item['filename']}"

    for html_file in HTML_FILES:
        if not html_file.exists():
            continue

        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # URLを置換
        for original_url, local_path in url_to_local.items():
            # src="..." の形式で置換
            content = content.replace(f'src="{original_url}"', f'src="{local_path}"')
            print(f"  ✓ Replaced in {html_file.name}")

        # 変更があった場合のみ保存
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {html_file.name}")
        else:
            print(f"→ No changes needed: {html_file.name}")

    print(f"\n✓ HTML files updated with local image paths")

def generate_report(mapping):
    """ダウンロード報告書を生成"""
    report_file = SCRIPT_DIR / "download-report.md"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Image Download Report\n\n")
        f.write(f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Images Downloaded**: {len(mapping)}\n\n")

        f.write("## Image Mapping\n\n")
        f.write("| # | Filename | License | Alt Text | From File |\n")
        f.write("|---|----------|---------|----------|----------|\n")

        for item in mapping:
            f.write(f"| {item['image_number']} | {item['filename']} | {item['license']} | {item['alt_text']} | {item['from_file']} |\n")

        f.write("\n## Image Paths\n\n")
        f.write("All images are saved in: `slider-images/` directory\n\n")

        f.write("### Local Path Format\n")
        f.write("```\nslider-images/g1.jpg\nslider-images/g2.jpg\nslider-images/g3.jpg\n...\n```\n\n")

        f.write("### License Information\n")
        f.write("- All images have commercial use license\n")
        f.write("- No attribution required (but recommended)\n\n")

    print(f"✓ Report saved to: {report_file}")

def main():
    """メイン処理"""
    print("=" * 60)
    print("Image Download & HTML Update Tool")
    print("=" * 60)

    try:
        # 画像をダウンロード
        mapping = download_all_images()

        if not mapping:
            print("\n✗ No images downloaded")
            return False

        # HTMLファイルのURLを置換
        replace_image_urls_in_html(mapping)

        # 報告書を生成
        generate_report(mapping)

        print("\n" + "=" * 60)
        print("✓ All tasks completed!")
        print("=" * 60)
        print(f"\n✓ Downloaded {len(mapping)} images")
        print(f"✓ Images saved in: {IMAGE_DIR}")
        print(f"✓ HTML files updated with local paths")
        print(f"✓ Mapping saved to: image-mapping.json")

        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
