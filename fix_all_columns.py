#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
import re
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = Path("C:/Users/taked/frontend-pomodoro")

# 各コラムの定義（目次、セクション、画像）
COLUMNS = {
    "02-regional-hiring.html": {
        "title": "■ 地方中小企業の人口流出を止める方法～地域創生と採用の関係性～",
        "target": "【ターゲット】地方採用に課題を持つ中小企業の経営者",
        "toc_items": [
            "導入",
            "地方企業が抱える採用課題",
            "地域を活かした採用戦略",
            "成功事例"
        ],
        "slider_images": ["g5.jpg", "g6.jpg", "g7.jpg", "g8.jpg"],
        "section_images": [
            ("【導入】", "g5.jpg"),
            ("【地方企業が抱える採用課題】", "g6.jpg"),
            ("【地域を活かした採用戦略】", "g7.jpg"),
            ("【成功事例】", "g8.jpg"),
        ]
    },
    "03-new-employee-retention.html": {
        "title": "■ 新入社員が辞める理由～早期離職を防ぐための対策～",
        "target": "【ターゲット】新入社員の離職に悩む企業の人事担当者",
        "toc_items": [
            "導入",
            "新入社員が辞める理由",
            "オンボーディング計画",
            "メンター制度と育成環境",
            "長期定着のための施策"
        ],
        "slider_images": ["g9.jpg", "g10.jpg", "g11.jpg", "g12.jpg"],
        "section_images": [
            ("【導入】", "g9.jpg"),
            ("【新入社員が辞める理由】", "g10.jpg"),
            ("【オンボーディング計画】", "g11.jpg"),
            ("【メンター制度と育成環境】", "g12.jpg"),
        ]
    },
    "04-midcareer-hiring.html": {
        "title": "■ 中途採用が失敗する理由～ミスマッチを防ぐための採用戦略～",
        "target": "【ターゲット】中途採用の定着に課題を持つ経営者",
        "toc_items": [
            "導入",
            "中途採用が失敗する理由",
            "ターゲット人材の定義と確保",
            "ジョブディスクリプションの活用",
            "オンボーディングと早期活躍"
        ],
        "slider_images": ["g13.jpg", "g14.jpg", "g15.jpg", "g16.jpg"],
        "section_images": [
            ("【導入】", "g13.jpg"),
            ("【中途採用が失敗する理由】", "g14.jpg"),
            ("【ターゲット人材の定義と確保】", "g15.jpg"),
            ("【ジョブディスクリプションの活用】", "g16.jpg"),
        ]
    },
    "05-recruitment-branding.html": {
        "title": "■ エンプロイヤーブランド～採用ブランディング戦略～",
        "target": "【ターゲット】採用力を強化したい中小企業経営者",
        "toc_items": [
            "導入",
            "エンプロイヤーブランドとは",
            "企業文化の発信と可視化",
            "社員の声を活かしたブランディング",
            "採用ブランドの成果測定"
        ],
        "slider_images": ["g17.jpg", "g18.jpg", "g19.jpg", "g20.jpg"],
        "section_images": [
            ("【導入】", "g17.jpg"),
            ("【エンプロイヤーブランドとは】", "g18.jpg"),
            ("【企業文化の発信と可視化】", "g19.jpg"),
            ("【社員の声を活かしたブランディング】", "g20.jpg"),
        ]
    }
}

def generate_toc_html(toc_items):
    """目次HTMLを生成"""
    items = "\n                ".join([f"<li>{item}</li>" for item in toc_items])
    return f"""        <div class="toc">
            <h2>【目次】</h2>
            <ol>
                {items}
            </ol>
        </div>"""

def generate_section_image(image_file, alt_text):
    """セクション画像HTMLを生成"""
    return f"""            <img src="slider-images/{image_file}" alt="{alt_text}" class="section-image">
            <div class="image-caption">{alt_text}</div>"""

def fix_column(filepath, config):
    """コラムを修復"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # タイトル置換
    html = re.sub(
        r'<h1>.*?</h1>',
        f'<h1>{config["title"]}</h1>',
        html,
        flags=re.DOTALL
    )

    # ターゲット置換
    html = re.sub(
        r'<div class="target">.*?</div>',
        f'<div class="target">{config["target"]}</div>',
        html,
        flags=re.DOTALL
    )

    # 目次置換
    new_toc = generate_toc_html(config["toc_items"])
    html = re.sub(
        r'        <div class="toc">.*?</div>',
        new_toc,
        html,
        flags=re.DOTALL
    )

    # スライダー画像置換
    for i, img_file in enumerate(config["slider_images"], 1):
        html = re.sub(
            rf'src="slider-images/g\d+\.jpg"',
            f'src="slider-images/{img_file}"',
            html,
            count=1
        )

    # セクション画像を各セクションの下に追加
    for section_title, image_file in config["section_images"]:
        # セクションタイトルを見つけて、その直後に画像を追加
        pattern = f'(<div class="section-title">{re.escape(section_title)}</div>)'
        section_image_html = generate_section_image(image_file, section_title.replace("【", "").replace("】", ""))

        # 既に画像がある場合はスキップ、なければ追加
        if f'<div class="section-title">{section_title}</div>\n            <img src="slider-images/{image_file}"' not in html:
            html = re.sub(
                pattern,
                f'\\1\n{section_image_html}',
                html
            )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Fixed: {filepath.name}")

# 修復実行
print("=" * 60)
print("Fixing all columns...")
print("=" * 60)

for filename, config in COLUMNS.items():
    filepath = SCRIPT_DIR / filename
    if filepath.exists():
        fix_column(filepath, config)
    else:
        print(f"✗ File not found: {filename}")

print("\n" + "=" * 60)
print("✓ All columns fixed!")
print("=" * 60)
