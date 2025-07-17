#!/usr/bin/env python3
"""
启动Web UI服务
"""

import subprocess
import sys
import os

def install_dependencies():
    """安装Web UI所需的依赖"""
    packages = ["fastapi", "uvicorn", "python-multipart"]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"❌ {package} 安装失败")

def main():
    print("🔧 PDFMark - 检查并安装依赖...")
    install_dependencies()
    
    print("\n🚀 启动PDFMark Web UI...")
    print("📱 请在浏览器中访问: http://localhost:8000")
    print("⏹️  按 Ctrl+C 停止服务")
    
    # 启动FastAPI应用
    os.system("python app.py")
    
if __name__ == "__main__":
    main()