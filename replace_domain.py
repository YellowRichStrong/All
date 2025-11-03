#!/usr/bin/env python3
import os
import re

# 要替换的域名
old_domain = 'oopenai2026.com'
new_domain = 'openai2026.com'

# 需要排除的文件和目录
exclude_files = ['replace_domain.py']  # 排除脚本本身
exclude_dirs = ['.git', 'node_modules', '__pycache__']

def replace_domain_in_file(file_path):
    """替换文件中的域名"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含旧域名
        if old_domain not in content:
            return False
        
        # 替换域名
        new_content = content.replace(old_domain, new_domain)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已更新: {file_path}")
        return True
    except Exception as e:
        print(f"处理文件时出错 {file_path}: {e}")
        return False

def process_directory(directory):
    """递归处理目录中的所有文件"""
    total_updated = 0
    
    for root, dirs, files in os.walk(directory):
        # 排除不需要处理的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # 排除不需要处理的文件
            if file in exclude_files:
                continue
            
            # 构建完整的文件路径
            file_path = os.path.join(root, file)
            
            # 处理文件
            if replace_domain_in_file(file_path):
                total_updated += 1
    
    return total_updated

if __name__ == "__main__":
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"开始替换域名: {old_domain} -> {new_domain}")
    print(f"处理目录: {script_dir}")
    
    # 处理目录
    total_updated = process_directory(script_dir)
    
    print(f"域名替换完成！共更新了 {total_updated} 个文件。")