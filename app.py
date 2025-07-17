#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF转Markdown Web应用
基于FastAPI构建的Web界面
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import fitz  # pymupdf
import re
import os
import tempfile
from pathlib import Path
import pandas as pd
from datetime import datetime

app = FastAPI(title="PDFMark - PDF转Markdown工具", description="PDFMark - PDF转Markdown工具", version="1.0.0")

# 创建静态文件目录
os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

def extract_text_with_pymupdf(pdf_path):
    """使用PyMuPDF提取PDF文本"""
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
    
    for line in lines:
        if not line.strip():
            processed_lines.append(line)
            continue
            
        # 检测数字编号标题
        if re.match(r'^\d+(\.\d+)*\.?\s+', line):
            level = line.count('.') + 1
            if level > 6:
                level = 6
            heading = '#' * level + ' ' + line
            processed_lines.append(heading)
        
        # 检测中文编号
        elif re.match(r'^[一二三四五六七八九十]+、', line):
            processed_lines.append('# ' + line)
        
        # 检测括号编号
        elif re.match(r'^\([一二三四五六七八九十\d]+\)', line):
            processed_lines.append('## ' + line)
        
        # 检测标题特征
        elif len(line) < 50 and (line.isupper() or '第' in line and '章' in line):
            processed_lines.append('# ' + line)
        
        else:
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def clean_markdown(text):
    """清理和优化Markdown格式"""
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = re.sub(r'(\n#{1,6}\s+.*)\n(?!\n)', r'\1\n\n', text)
    text = re.sub(r'(?<!\n)\n(#{1,6}\s+.*)', r'\n\n\1', text)
    return text

@app.get("/", response_class=HTMLResponse)
async def main():
    """主页面"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PDF转Markdown工具</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            .upload-area {
                border: 2px dashed #ddd;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                margin: 20px 0;
                transition: border-color 0.3s;
            }
            .upload-area:hover {
                border-color: #007bff;
            }
            .upload-btn {
                background: #007bff;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            .upload-btn:hover {
                background: #0056b3;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .success {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }
            .error {
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }
            .loading {
                text-align: center;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 PDF转Markdown工具</h1>
            <p style="text-align: center; color: #666;">
                上传PDF文件，自动转换为保留层级结构的Markdown格式
            </p>
            
            <div class="upload-area">
                <form id="uploadForm" enctype="multipart/form-data">
                    <input type="file" id="fileInput" name="file" accept=".pdf" style="display: none;">
                    <div onclick="document.getElementById('fileInput').click()">
                        <p>📁 点击选择PDF文件</p>
                        <p style="color: #999; font-size: 14px;">支持格式：PDF</p>
                    </div>
                    <button type="submit" class="upload-btn" style="margin-top: 15px;">
                        🚀 开始转换
                    </button>
                </form>
            </div>
            
            <div id="result" class="result"></div>
        </div>

        <script>
            document.getElementById('fileInput').addEventListener('change', function(e) {
                const fileName = e.target.files[0]?.name;
                if (fileName) {
                    document.querySelector('.upload-area p').textContent = `已选择: ${fileName}`;
                }
            });

            document.getElementById('uploadForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const fileInput = document.getElementById('fileInput');
                const resultDiv = document.getElementById('result');
                
                if (!fileInput.files[0]) {
                    resultDiv.className = 'result error';
                    resultDiv.textContent = '请先选择PDF文件';
                    resultDiv.style.display = 'block';
                    return;
                }
                
                // 显示加载状态
                resultDiv.className = 'result loading';
                resultDiv.innerHTML = '⏳ 正在转换中，请稍候...';
                resultDiv.style.display = 'block';
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                try {
                    const response = await fetch('/convert', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = `
                            ✅ 转换成功！<br>
                            <a href="/download/${result.filename}" download style="color: #007bff; text-decoration: none;">
                                📥 下载Markdown文件
                            </a>
                        `;
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.textContent = `❌ 转换失败: ${result.detail}`;
                    }
                } catch (error) {
                    resultDiv.className = 'result error';
                    resultDiv.textContent = `❌ 网络错误: ${error.message}`;
                }
            });
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    """转换PDF为Markdown"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="请上传PDF文件")
    
    try:
        # 保存上传的文件
        upload_path = f"uploads/{file.filename}"
        with open(upload_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 提取文本
        text = extract_text_with_pymupdf(upload_path)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF文件无法提取文本内容")
        
        # 转换为Markdown
        markdown_text = detect_headings(text)
        markdown_text = clean_markdown(markdown_text)
        
        # 添加文档头部
        pdf_name = Path(file.filename).stem
        header = f"""# {pdf_name}

> 本文档由PDF自动转换生成
> 原文件：{file.filename}
> 转换时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        markdown_text = header + markdown_text
        
        # 保存Markdown文件
        output_filename = f"{pdf_name}.md"
        output_path = f"outputs/{output_filename}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        
        # 清理上传的PDF文件
        os.remove(upload_path)
        
        return {"message": "转换成功", "filename": output_filename}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转换过程中出现错误: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """下载转换后的Markdown文件"""
    file_path = f"outputs/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='text/markdown'
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动PDF转Markdown Web服务...")
    print("📱 访问地址: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)