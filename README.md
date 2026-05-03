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
4. **重新打包** - 处理完成后重新打包为 epub 文件

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

## 项目结构

```
.
├── README.md          # 项目说明
├── book_pinyin.py     # 主程序
├── requirements.txt   # 依赖库列表
└── test_pinyin.py     # 测试脚本（可选）
```

## 致谢

感谢所有开源库的作者及其贡献者们！

## 许可证

本项目为开源项目，欢迎使用和贡献。

## 贡献

欢迎提交 Issue 和 Pull Request！
