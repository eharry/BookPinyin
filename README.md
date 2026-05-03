# Book Pinyin - 电子书拼音加注工具

为 epub 和 mobi 格式的中文电子书自动添加拼音注音的 Python 工具。

## 关于项目开发

本项目代码完全由 Trae AI 开发，项目贡献者参与了最终拼音效果的验证工作。

## 功能特性

- 支持 epub 格式电子书
- 支持 mobi 格式电子书（自动转换为 epub 输出）
- 自动为所有汉字添加拼音注音
- 使用 HTML `<ruby>` 标签实现美观的注音显示
- 输出文件名自动追加 `—注音版` 后缀
- 自动更新 epub 元数据，书名后添加 `—注音版`
- 严格遵守 epub 打包规范，确保设备兼容性

## 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖库

- `pypinyin>=0.49.0` - 汉字转拼音
- `lxml>=4.9.0` - HTML 处理
- `mobi>=0.4.0` - mobi 文件提取

## 使用方法

### 基本用法

```bash
python book_pinyin.py <输入文件路径> [输出文件路径]
```

### 示例

#### 转换 epub 文件
```bash
python book_pinyin.py my_book.epub
# 输出: my_book—注音版.epub
```

#### 转换 mobi 文件
```bash
python book_pinyin.py my_book.mobi
# 输出: my_book—注音版.epub
```

#### 指定输出路径
```bash
python book_pinyin.py input.epub /path/to/output.epub
```

## 原理说明

1. **解压文件** - epub/mobi 文件本质上是压缩包，先解压
2. **处理 HTML** - 遍历所有 HTML/XHTML 文件
3. **添加拼音** - 为文本中的汉字添加 `<ruby>` 标签格式的拼音
4. **更新元数据** - 自动在书名后添加 `—注音版` 标识
5. **重新打包** - 严格遵守 epub 规范重新打包，确保设备兼容性

### 拼音格式

使用 HTML 标准的 ruby 标签：
```html
<ruby>汉字<rt>pinyin</rt></ruby>
```

## 关键第三方库

本项目依赖以下优秀的开源项目，在此表示感谢：

- [pypinyin](https://github.com/mozillazg/python-pinyin) - 汉字转拼音的 Python 库
- [lxml](https://lxml.de/) - 功能强大的 XML 和 HTML 处理库
- [mobi](https://github.com/iscc/mobi) - mobi 文件提取和处理库

## 注意事项

- 目前仅支持中文文本的拼音标注
- 不处理 DRM 加密的电子书
- 建议先备份原文件
- 转换后的 epub 文件会添加 CSS 样式以确保拼音正确显示

## 已知问题

- **KOReader**：可以正常显示拼音，但打开书籍时可能会有些慢（因为添加了拼音标签和样式）
- **Send to Kindle**：通过 Send to Kindle 推送可能会失败（原因尚不明确，可能与文件大小或结构有关）

## Kindle 使用建议

**如果想要在 Kindle 设备上使用转换后的注音版电子书：**

由于 KOReader 对拼音标注（`<ruby>` 标签）支持不好，可能导致显示不正常。**推荐解决方案：**

> **使用 Calibre 将转换后的 epub 文件转换为 mobi 格式，然后复制到 Kindle 设备上，使用 Kindle 原生系统打开。Kindle 原生系统可以更好地打开文件并展示拼音。**

具体步骤：
1. 使用本工具将原始电子书转换为带拼音的 epub 文件
2. 打开 Calibre，添加转换后的 epub 文件
3. 右键点击书籍，选择"转换书籍"→"转换为 MOBI"
4. 将转换后的 mobi 文件通过 USB 复制到 Kindle 设备
5. 使用 Kindle 原生系统打开阅读

## 项目结构

```
.
├── README.md          # 项目说明
├── book_pinyin.py     # 主程序
├── requirements.txt   # 依赖库列表
└── test_pinyin.py     # 测试脚本（可选）
```

## 致谢

- 感谢所有开源库的作者及其贡献者们！
- 特别感谢 [Trae AI](https://trae.ai/) 提供免费的 AI 功能，使本项目得以开发完成！

## 许可证

本项目为开源项目，欢迎使用和贡献。

## 贡献

欢迎提交 Issue 和 Pull Request！
