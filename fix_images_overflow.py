#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像オーバーフロー修正 + コラム1に画像追加
"""
import sys
import io
import re
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = Path("C:/Users/taked/frontend-pomodoro")

def fix_css_all_columns():
    """すべてのコラムの CSS を修正"""
    files = [
        "01-hiring-trends.html",
        "02-regional-hiring.html",
        "03-new-employee-retention.html",
        "04-midcareer-hiring.html",
        "05-recruitment-branding.html",
    ]

    for filename in files:
        filepath = SCRIPT_DIR / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # CSS の @media (max-width: 768px) の前に image-container スタイルを追加
        new_css = '''        .image-container {
            width: 100%;
            max-width: 100%;
            margin: 20px 0;
            overflow: hidden;
        }

        '''

        if '.image-container' not in content:
            # @media の前に追加
            content = re.sub(
                r'(        @media \(max-width:)',
                new_css + r'\1',
                content
            )

        # section-image の CSS を修正
        content = re.sub(
            r'\.section-image\s*\{([^}]*)\n\s*width:\s*100%;',
            r'.section-image {\1\n            width: 100%;\n            max-width: 100%;',
            content
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Fixed CSS in {filename}")

def add_section_images_to_column1():
    """コラム1 にセクション画像を追加"""
    filepath = SCRIPT_DIR / "01-hiring-trends.html"

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # セクション画像を追加する位置と内容を定義
    # 各セクションタイトルの直後に画像を追加
    replacements = [
        (
            '(<div class="section-title">【導入】</div>)',
            r'\1\n            <div class="image-container"><img src="slider-images/g1.jpg" alt="導入" class="section-image"><div class="image-caption">採用トレンド</div></div>'
        ),
        (
            '(<div class="section-title">【1つ目のトレンド：「企業のストーリー」が採用力を左右する時代】</div>)',
            r'\1\n            <div class="image-container"><img src="slider-images/g2.jpg" alt="企業ストーリー" class="section-image"><div class="image-caption">企業ストーリーが採用力を左右</div></div>'
        ),
        (
            '(<div class="section-title">【2つ目のトレンド：「働き方の多様性」が採用競争力になる】</div>)',
            r'\1\n            <div class="image-container"><img src="slider-images/g3.jpg" alt="働き方の多様性" class="section-image"><div class="image-caption">働き方の多様性が競争力に</div></div>'
        ),
        (
            '(<div class="section-title">【3つ目のトレンド：「採用」は一時的ではなく「継続的な発信」の時代】</div>)',
            r'\1\n            <div class="image-container"><img src="slider-images/g4.jpg" alt="継続的な採用発信" class="section-image"><div class="image-caption">継続的な採用発信が重要</div></div>'
        ),
    ]

    for pattern, replacement in replacements:
        # 既に画像がない場合のみ追加
        if 'image-container' not in content.split(pattern)[1].split('</div>')[0]:
            content = re.sub(pattern, replacement, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Added section images to column 1")

# 実行
print("=" * 60)
print("Fixing image overflow and adding section images")
print("=" * 60)

fix_css_all_columns()
print()
add_section_images_to_column1()

print("\n" + "=" * 60)
print("✓ All fixes completed!")
print("=" * 60)
