#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本用于检查所有HTML文件中是否包含Google AdSense脚本，并为缺少的文件添加该脚本
"""

import os
import re

def add_adsense_script():
    # 定义AdSense脚本
    adsense_script = '    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6486368477427533"\n      crossorigin="anonymous"></script>'
    
    # 要搜索的目录
    base_dir = "/Users/macbookpro/Desktop/trae/oopenai2026"
    
    # 统计信息
    total_files = 0
    files_with_script = 0
    files_added_script = 0
    
    # 遍历所有HTML文件
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                total_files += 1
                file_path = os.path.join(root, file)
                
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查是否已包含AdSense脚本
                    if 'ca-pub-6486368477427533' in content:
                        files_with_script += 1
                        print(f"✓ {file_path} 已包含AdSense脚本")
                        continue
                    
                    # 检查是否有head标签
                    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
                    if not head_match:
                        print(f"! {file_path} 没有找到head标签")
                        continue
                    
                    # 在head标签的末尾添加脚本（在</head>之前）
                    head_content = head_match.group(1)
                    new_head_content = head_content.rstrip() + '\n' + adsense_script
                    new_content = content.replace(f'<head>{head_content}</head>', f'<head>{new_head_content}</head>')
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    files_added_script += 1
                    print(f"+ {file_path} 已添加AdSense脚本")
                    
                except Exception as e:
                    print(f"! 处理 {file_path} 时出错: {e}")
    
    # 打印统计信息
    print("\n===== 统计结果 =====")
    print(f"总共检查的HTML文件: {total_files}")
    print(f"已包含AdSense脚本的文件: {files_with_script}")
    print(f"新增AdSense脚本的文件: {files_added_script}")
    print(f"未处理的文件: {total_files - files_with_script - files_added_script}")
    print("==================")

if __name__ == "__main__":
    print("开始检查并添加Google AdSense脚本...\n")
    add_adsense_script()
    print("\n处理完成!")