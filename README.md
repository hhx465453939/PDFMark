# PDFMark 📄➡️📝

[English](#english) | [中文](#中文)

---

## 中文

### 📖 项目简介

**PDFMark** 是一个功能强大的PDF转Markdown转换工具，支持命令行和Web界面两种使用方式，能够智能识别文档结构并保留原有的层级格式。特别适用于学术论文、技术文档和规范性文件的格式转换。

### ✨ 特性

- 🎯 **智能标题识别**：自动检测数字编号、中文编号、括号编号等多种标题格式
- 📊 **层级结构保留**：完整保持原文档的章节层级关系
- 🌐 **双重界面**：支持命令行脚本和Web UI两种使用方式
- 🔧 **格式优化**：自动清理多余空行，优化列表和段落格式
- 🚀 **高效转换**：基于PyMuPDF，转换速度快且准确度高
- 🎨 **现代化UI**：响应式Web界面，支持拖拽上传
- 📱 **跨平台**：支持Windows、macOS、Linux
- 🌍 **中文友好**：完美支持中文文档和编号格式

### 🛠️ 安装依赖

#### 方法一：自动安装（推荐）
```bash
python install_requirements.py
```

#### 方法二：手动安装
```bash
pip install PyPDF2 PyMuPDF pandas fastapi uvicorn python-multipart
```

### 🚀 使用方法

#### 命令行版本

1. **基本使用**：
```bash
python pdf_to_markdown.py
```

2. **自定义输入文件**：
```python
# 修改 pdf_to_markdown.py 中的文件名
pdf_file = "你的PDF文件.pdf"
```

#### Web UI版本

1. **启动Web服务**：
```bash
python start_webui.py
```

2. **访问Web界面**：
   - 在浏览器中打开：`http://localhost:8000`
   - 上传PDF文件
   - 点击"开始转换"
   - 下载生成的Markdown文件

### 📁 项目结构

```
PDFMark/
├── README.md                    # 项目说明文档
├── install_requirements.py     # 依赖安装脚本
├── pdf_to_markdown.py          # 命令行转换脚本
├── app.py                      # Web UI应用
├── start_webui.py              # Web UI启动脚本
├── uploads/                    # 上传文件临时目录
├── outputs/                    # 转换结果输出目录
└── static/                     # 静态资源目录
```

### 🎯 支持的标题格式

工具能够智能识别以下标题格式：

- **数字编号**：`1.` `2.1` `3.2.1` 等
- **中文编号**：`一、` `二、` `三、` 等
- **括号编号**：`(1)` `(2)` `(一)` `(二)` 等
- **章节标题**：包含"第X章"等关键词的标题
- **全大写标题**：短行全大写文本

### 📋 转换示例

#### 输入PDF内容：
```
第一章 绪论

1.1 研究背景
1.1.1 问题提出
1.1.2 研究意义

1.2 研究目标
(1) 主要目标
(2) 次要目标

二、文献综述
```

#### 输出Markdown：
```markdown
# 第一章 绪论

## 1.1 研究背景
### 1.1.1 问题提出
### 1.1.2 研究意义

## 1.2 研究目标
### (1) 主要目标
### (2) 次要目标

# 二、文献综述
```

### ⚙️ 配置选项

#### 自定义标题检测规则

在 `detect_headings()` 函数中可以自定义标题识别规则：

```python
# 添加新的标题格式检测
elif re.match(r'^第[一二三四五六七八九十]+节', line):
    processed_lines.append('## ' + line)
```

### 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

---

## English

### 📖 Project Description

**PDFMark** is a powerful PDF to Markdown conversion tool that supports both command-line and web interface usage. It intelligently recognizes document structure and preserves the original hierarchical formatting. Particularly suitable for academic papers, technical documentation, and regulatory documents.

### ✨ Features

- 🎯 **Smart Title Recognition**: Automatically detects various title formats including numeric numbering, Chinese numbering, parenthetical numbering, etc.
- 📊 **Hierarchy Preservation**: Completely maintains the chapter and section hierarchy of the original document
- 🌐 **Dual Interface**: Supports both command-line scripts and Web UI
- 🔧 **Format Optimization**: Automatically cleans up extra blank lines and optimizes list and paragraph formatting
- 🚀 **Efficient Conversion**: Based on PyMuPDF for fast and accurate conversion
- 🎨 **Modern UI**: Responsive web interface with drag-and-drop upload support
- 📱 **Cross-platform**: Supports Windows, macOS, Linux
- 🌍 **Chinese-friendly**: Perfect support for Chinese documents and numbering formats

### 🛠️ Installation

#### Method 1: Automatic Installation (Recommended)
```bash
python install_requirements.py
```

#### Method 2: Manual Installation
```bash
pip install PyPDF2 PyMuPDF pandas fastapi uvicorn python-multipart
```

### 🚀 Usage

#### Command Line Version

1. **Basic Usage**:
```bash
python pdf_to_markdown.py
```

2. **Custom Input File**:
```python
# Modify the filename in pdf_to_markdown.py
pdf_file = "your_pdf_file.pdf"
```

#### Web UI Version

1. **Start Web Service**:
```bash
python start_webui.py
```

2. **Access Web Interface**:
   - Open in browser: `http://localhost:8000`
   - Upload PDF file
   - Click "Start Conversion"
   - Download the generated Markdown file

### 📁 Project Structure

```
PDFMark/
├── README.md                    # Project documentation
├── install_requirements.py     # Dependency installation script
├── pdf_to_markdown.py          # Command-line conversion script
├── app.py                      # Web UI application
├── start_webui.py              # Web UI startup script
├── uploads/                    # Temporary upload directory
├── outputs/                    # Conversion output directory
└── static/                     # Static resources directory
```

### 🎯 Supported Title Formats

The tool can intelligently recognize the following title formats:

- **Numeric Numbering**: `1.` `2.1` `3.2.1` etc.
- **Chinese Numbering**: `一、` `二、` `三、` etc.
- **Parenthetical Numbering**: `(1)` `(2)` `(一)` `(二)` etc.
- **Chapter Titles**: Titles containing keywords like "Chapter X"
- **All-caps Titles**: Short lines of all-uppercase text

### 📋 Conversion Example

#### Input PDF Content:
```
Chapter 1 Introduction

1.1 Research Background
1.1.1 Problem Statement
1.1.2 Research Significance

1.2 Research Objectives
(1) Primary Objectives
(2) Secondary Objectives

II. Literature Review
```

#### Output Markdown:
```markdown
# Chapter 1 Introduction

## 1.1 Research Background
### 1.1.1 Problem Statement
### 1.1.2 Research Significance

## 1.2 Research Objectives
### (1) Primary Objectives
### (2) Secondary Objectives

# II. Literature Review
```

### ⚙️ Configuration Options

#### Custom Title Detection Rules

You can customize title recognition rules in the `detect_headings()` function:

```python
# Add new title format detection
elif re.match(r'^Section [IVXLCDM]+', line):
    processed_lines.append('## ' + line)
```

### 🤝 Contributing

Issues and Pull Requests are welcome to improve the project!

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

### 🌟 Star History

If this project helps you, please consider giving it a star! ⭐

### 📞 Contact

- Issues: [GitHub Issues](https://github.com/yourusername/PDFMark/issues)
- Email: your.email@example.com

---

**PDFMark** - Making PDF to Markdown conversion simple and intelligent! 🚀
