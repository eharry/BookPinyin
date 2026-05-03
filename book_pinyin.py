#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Book Pinyin - 电子书拼音加注工具
为 epub/mobi 文件中的中文文本添加拼音注音
支持 epub 和 mobi 格式
"""

import os
import sys
import zipfile
import shutil
import re
from pathlib import Path
from pypinyin import pinyin, Style


def is_chinese_char(char):
    """判断是否是中文字符"""
    return '\u4e00' <= char <= '\u9fff'


def add_pinyin_to_text(text):
    """为文本中的汉字添加拼音注音"""
    result = []
    i = 0
    n = len(text)

    while i < n:
        if is_chinese_char(text[i]):
            chinese_chars = []
            while i < n and is_chinese_char(text[i]):
                chinese_chars.append(text[i])
                i += 1

            pinyin_list = pinyin(''.join(chinese_chars), style=Style.TONE)

            for char, py in zip(chinese_chars, pinyin_list):
                result.append(f'<ruby>{char}<rt>{py[0]}</rt></ruby>')
        else:
            result.append(text[i])
            i += 1

    return ''.join(result)


def process_html_content(html_content):
    """处理 HTML 内容，只在正文文本中添加拼音，跳过特定标签"""
    result = []
    i = 0
    n = len(html_content)
    skip_tags = {'title', 'script', 'style', 'head'}
    current_skip = False

    while i < n:
        if html_content[i] == '<':
            # 处理标签
            tag_start = i
            end = html_content.find('>', i)
            if end == -1:
                result.append(html_content[i:])
                break
            tag_str = html_content[i:end+1]
            result.append(tag_str)

            # 检查标签类型
            if not current_skip:
                # 检查是否进入了需要跳过的标签
                tag_name = tag_str.strip('<>/').split()[0].lower()
                if tag_name in skip_tags:
                    current_skip = tag_name
            else:
                # 检查是否离开当前跳过的标签
                tag_name = tag_str.strip('<>/').split()[0].lower()
                if tag_name == current_skip:
                    current_skip = False

            i = end + 1
        else:
            # 处理文本
            start = i
            while i < n and html_content[i] != '<':
                i += 1
            text = html_content[start:i]
            if not current_skip:
                result.append(add_pinyin_to_text(text))
            else:
                result.append(text)

    return ''.join(result)


def process_html_files_in_dir(temp_dir):
    """处理目录中的所有 HTML 文件"""
    html_files = list(temp_dir.rglob('*.html')) + list(temp_dir.rglob('*.xhtml'))

    for html_file in html_files:
        print(f"处理文件: {html_file}")
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        processed_content = process_html_content(content)

        # 添加 ruby 样式 - display:block + ruby-position:over 混合方式
        if '</head>' in processed_content:
            ruby_style = '''
<style type="text/css">
ruby {
    display: inline-block;
    text-align: center;
    vertical-align: text-top;
}
rt {
    display: block;
    font-size: 60%;
    line-height: 1.1;
    ruby-position: over;
    margin-bottom: -0.2em;
}
</style>
</head>'''
            processed_content = processed_content.replace('</head>', ruby_style)

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)


def update_metadata(temp_dir):
    """更新 epub 文件的元数据，在书名后添加'—注音版'"""
    opf_files = list(temp_dir.rglob('content.opf')) + list(temp_dir.rglob('*.opf'))

    if not opf_files:
        print("警告: 未找到 metadata 文件")
        return

    opf_file = opf_files[0]
    print(f"更新元数据: {opf_file}")

    with open(opf_file, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_title(match):
        tag_start = match.group(1)
        title = match.group(2)
        tag_end = match.group(3)
        if '—注音版' not in title:
            new_title = title + '—注音版'
            return f'{tag_start}{new_title}{tag_end}'
        return match.group(0)

    content = re.sub(r'(<dc:title[^>]*>)(.*?)(</dc:title>)', replace_title, content, flags=re.DOTALL)
    content = re.sub(r'(<title[^>]*>)(.*?)(</title>)', replace_title, content, flags=re.DOTALL)

    with open(opf_file, 'w', encoding='utf-8') as f:
        f.write(content)


def repack_epub(temp_dir, output_path):
    """重新打包成 epub 文件，严格遵守 epub 规范"""
    # epub 规范要求：
    # 1. mimetype 文件必须不压缩，且必须是第一个文件
    # 2. 文件按特定顺序打包

    # 收集所有文件
    all_files = []
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = Path(root) / file
            arcname = str(file_path.relative_to(temp_dir))
            all_files.append((file_path, arcname))

    # 按 epub 规范排序：mimetype > META-INF > 其他文件
    def sort_key(item):
        arcname = item[1]
        if arcname == 'mimetype':
            return (0, arcname)
        elif arcname.startswith('META-INF/'):
            return (1, arcname)
        else:
            return (2, arcname)

    all_files.sort(key=sort_key)

    # 创建新的 epub 文件
    with zipfile.ZipFile(output_path, 'w') as zf:
        for file_path, arcname in all_files:
            if arcname == 'mimetype':
                # mimetype 必须不压缩
                zf.write(file_path, arcname, compress_type=zipfile.ZIP_STORED)
            else:
                # 其他文件使用 deflate 压缩
                zf.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)


def process_epub(input_path, output_path=None):
    """处理 epub 文件"""
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = input_path_obj.parent / f"{input_path_obj.stem}—注音版{input_path_obj.suffix}"

    temp_dir = Path("temp_epub")
    temp_dir.mkdir(exist_ok=True)

    try:
        with zipfile.ZipFile(input_path, 'r') as zf:
            zf.extractall(temp_dir)

        process_html_files_in_dir(temp_dir)
        update_metadata(temp_dir)
        repack_epub(temp_dir, output_path)

        print(f"\n处理完成！输出文件: {output_path}")
        return output_path

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


def process_mobi(input_path, output_path=None):
    """处理 mobi 文件"""
    import mobi

    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = input_path_obj.parent / f"{input_path_obj.stem}—注音版.epub"

    temp_dir = Path("temp_mobi")
    temp_dir.mkdir(exist_ok=True)

    try:
        print("正在提取 mobi 文件...")
        mobi_temp_dir, extracted_file = mobi.extract(input_path)

        shutil.move(mobi_temp_dir, temp_dir)

        if extracted_file and Path(extracted_file).exists():
            ext = Path(extracted_file).suffix.lower()
            if ext == '.epub':
                epub_dir = temp_dir / "epub_content"
                epub_dir.mkdir(exist_ok=True)
                with zipfile.ZipFile(extracted_file, 'r') as zf:
                    zf.extractall(epub_dir)
                temp_dir = epub_dir

        process_html_files_in_dir(temp_dir)
        update_metadata(temp_dir)
        repack_epub(temp_dir, output_path)

        print(f"\n处理完成！输出文件: {output_path}")
        return output_path

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


def main():
    if len(sys.argv) < 2:
        print("使用方法: python book_pinyin.py <文件路径> [输出文件路径]")
        print("支持的格式: .epub, .mobi")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_path):
        print(f"错误: 文件不存在 - {input_path}")
        sys.exit(1)

    ext = Path(input_path).suffix.lower()

    if ext == '.epub':
        process_epub(input_path, output_path)
    elif ext == '.mobi':
        process_mobi(input_path, output_path)
    else:
        print(f"错误: 不支持的文件格式 {ext}，仅支持 .epub 和 .mobi")
        sys.exit(1)


if __name__ == "__main__":
    main()
