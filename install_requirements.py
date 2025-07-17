#!/usr/bin/env python3
"""
安装PDF转换所需的依赖包
"""

import subprocess
import sys

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} 安装成功")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {package} 安装失败")
        return False

def main():
    """主安装函数"""
    print("正在安装PDF转换所需的依赖包...")
    
    packages = [
        "PyPDF2",
        "PyMuPDF",  # fitz
        "pandas"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n安装完成: {success_count}/{len(packages)} 个包安装成功")
    
    if success_count == len(packages):
        print("🎉 所有依赖包安装完成，可以运行PDF转换脚本了！")
    else:
        print("⚠️  部分包安装失败，请手动安装")

if __name__ == "__main__":
    main()