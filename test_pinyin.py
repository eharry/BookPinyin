#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试拼音功能
"""

from epub_pinyin import add_pinyin_to_text, process_html_content

test_text = "你好，世界！这是一个测试。"
print(f"原始文本: {test_text}")
print(f"添加拼音后: {add_pinyin_to_text(test_text)}")

test_html = """
<html>
<body>
    <h1>测试标题</h1>
    <p>这是第一段文本。</p>
    <p>这是第二段文本，包含中文和English混合。</p>
</body>
</html>
"""
print("\n--- HTML 测试 ---")
print(f"原始 HTML:\n{test_html}")
processed_html = process_html_content(test_html)
print(f"\n处理后 HTML:\n{processed_html}")
