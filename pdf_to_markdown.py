#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF转Markdown脚本
功能：将PDF文件转换为保留层级结构的Markdown文件
"""

import PyPDF2
import fitz  # pymupdf
import re
import os
from pathlib import Path

def extract_text_with_pymupdf(pdf_path):
    """使用PyMuPDF提取PDF文本，保留更好的格式"""
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        full_text += f"\n<!-- 第{page_num + 1}页 -->\n"
        full_text += text + "\n"
    
    doc.close()
    return full_text

def detect_headings(text):
    """检测标题层级"""
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:  # 修复：移除错误的 .strip()
        if not line.strip():
            processed_lines.append(line)
            continue
            
        # 检测数字编号标题 (如: 1. 2.1 3.2.1)
        if re.match(r'^\d+(\.\d+)*\.?\s+', line):
            level = line.count('.') + 1
            if level > 6:
                level = 6
            heading = '#' * level + ' ' + line
            processed_lines.append(heading)
        
        # 检测中文编号 (如: 一、二、三、)
        elif re.match(r'^[一二三四五六七八九十]+、', line):
            processed_lines.append('# ' + line)
        
        # 检测括号编号 (如: (1) (2) (一) (二))
        elif re.match(r'^\([一二三四五六七八九十\d]+\)', line):
            processed_lines.append('## ' + line)
        
        # 检测全大写或加粗标题特征
        elif len(line) < 50 and (line.isupper() or '第' in line and '章' in line):
            processed_lines.append('# ' + line)
        
        else:
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def clean_markdown(text):
    """清理和优化Markdown格式"""
    # 移除多余的空行
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    
    # 确保标题前后有适当的空行
    text = re.sub(r'(\n#{1,6}\s+.*)\n(?!\n)', r'\1\n\n', text)
    text = re.sub(r'(?<!\n)\n(#{1,6}\s+.*)', r'\n\n\1', text)
    
    # 处理列表格式
    text = re.sub(r'\n(\d+\.\s+)', r'\n\1', text)
    text = re.sub(r'\n([•·-]\s+)', r'\n\1', text)
    
    return text

def pdf_to_markdown(pdf_path, output_path=None):
    """主函数：PDF转Markdown"""
    if not os.path.exists(pdf_path):
        print(f"错误：文件 {pdf_path} 不存在")
        return False
    
    print(f"正在处理: {pdf_path}")
    
    try:
        # 提取文本
        text = extract_text_with_pymupdf(pdf_path)
        
        if not text.strip():
            print("警告：未能提取到文本内容")
            return False
        
        # 检测和转换标题
        markdown_text = detect_headings(text)
        
        # 清理格式
        markdown_text = clean_markdown(markdown_text)
        
        # 添加文档头部
        pdf_name = Path(pdf_path).stem
        header = f"""# {pdf_name}

> 本文档由PDF自动转换生成
> 原文件：{pdf_path}
> 转换时间：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        markdown_text = header + markdown_text
        
        # 确定输出路径
        if output_path is None:
            output_path = pdf_path.replace('.pdf', '.md')
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        
        print(f"转换完成！输出文件: {output_path}")
        return True
        
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")
        return False

if __name__ == "__main__":
    import pandas as pd
    
    # 目标PDF文件
    pdf_file = "附件1南京农业大学研究生学位论文格式规范（自然科学类）.pdf"
    
    # 检查文件是否存在
    if os.path.exists(pdf_file):
        # 执行转换
        success = pdf_to_markdown(pdf_file)
        
        if success:
            print("\n✅ PDF转Markdown完成！")
            print(f"📄 输出文件: {pdf_file.replace('.pdf', '.md')}")
        else:
            print("\n❌ 转换失败，请检查错误信息")
    else:
        print(f"❌ 错误：找不到文件 {pdf_file}")
        print("请确保脚本在正确的目录中运行")
