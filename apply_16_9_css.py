#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
すべてのコラムに 16:9 アスペクト比 CSS を適用
"""
import sys
import io
import re
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = Path("C:/Users/taked/frontend-pomodoro")
FILES = [
    "02-regional-hiring.html",
    "03-new-employee-retention.html",
    "04-midcareer-hiring.html",
    "05-recruitment-branding.html",
]

def apply_16_9_css(filepath):
    """16:9 アスペクト比 CSS を適用"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # .swiper の高さ固定を aspect-ratio に変更
    content = re.sub(
        r'\.swiper\s*\{\s*width:\s*100%;\s*height:\s*\d+px;',
        '.swiper {\n            width: 100%;\n            aspect-ratio: 16 / 9;',
        content
    )

    # .swiper-slide に aspect-ratio を追加
    if 'aspect-ratio: 16 / 9' not in content or '.swiper-slide' not in content:
        content = re.sub(
            r'(\.swiper-slide\s*\{[^}]*background-color:\s*#f5f5f5;)',
            r'\1\n            aspect-ratio: 16 / 9;',
            content
        )

    # .swiper-slide img の object-fit を contain から cover に変更
    content = re.sub(
        r'\.swiper-slide img\s*\{[^}]*object-fit:\s*contain;',
        '.swiper-slide img {\n            width: 100%;\n            height: 100%;\n            object-fit: cover;',
        content
    )

    # .section-image に aspect-ratio と object-fit を追加
    if '.section-image' in content:
        content = re.sub(
            r'(\.section-image\s*\{[^}]*width:\s*100%;)\s*height:\s*auto;',
            r'\1\n            aspect-ratio: 16 / 9;',
            content
        )

        # section-image に object-fit を追加
        if 'object-fit: cover' not in content.split('.section-image')[1].split('}')[0]:
            content = re.sub(
                r'(\.section-image\s*\{[^}]*display:\s*block;)',
                r'\1\n            object-fit: cover;',
                content
            )

    # メディアクエリの .swiper を修正
    content = re.sub(
        r'@media.*?\{[^}]*\.swiper\s*\{[^}]*height:\s*\d+px;',
        lambda m: m.group(0).replace('height:', 'aspect-ratio: 16 / 9; /* old height:'),
        content,
        flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Applied 16:9 CSS to {filepath.name}")

print("=" * 60)
print("Applying 16:9 aspect ratio CSS to all columns")
print("=" * 60)

for filename in FILES:
    filepath = SCRIPT_DIR / filename
    if filepath.exists():
        apply_16_9_css(filepath)
    else:
        print(f"✗ File not found: {filename}")

print("\n" + "=" * 60)
print("✓ 16:9 aspect ratio applied to all columns!")
print("=" * 60)
