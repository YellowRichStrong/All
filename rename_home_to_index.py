#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# 替换函数
def replace_home_with_index(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换所有出现的"index"为"index"
        new_content = content.replace('index', 'index')
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

# 遍历目录函数
def process_directory(directory):
    changed_count = 0
    processed_count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.py')):  # 处理HTML和Python文件
                file_path = os.path.join(root, file)
                processed_count += 1
                if replace_home_with_index(file_path):
                    changed_count += 1
                    print(f"已更新: {file_path}")
    
    print(f"\n处理完成！")
    print(f"总共处理了 {processed_count} 个文件")
    print(f"成功更新了 {changed_count} 个文件")

if __name__ == "__main__":
    # 从当前目录开始处理
    directory = os.path.dirname(os.path.abspath(__file__))
    print(f"开始处理目录: {directory}")
    process_directory(directory)