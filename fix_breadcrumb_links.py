#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# 设置tools目录路径
tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'

# 定义要查找和替换的模式
pattern = r'<a href="\.\./image\.html">Image Tools</a>'
replacement = '<a href="../index.html">Image Tools</a>'

# 统计修复的文件数
fixed_files = 0
failed_files = 0

# 遍历tools目录下的所有HTML文件
for filename in os.listdir(tools_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(tools_dir, filename)
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 检查是否需要替换
            if re.search(pattern, content):
                # 执行替换
                new_content = re.sub(pattern, replacement, content)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                
                fixed_files += 1
                print(f"修复了文件: {filename}")
        
        except Exception as e:
            failed_files += 1
            print(f"处理文件 {filename} 时出错: {str(e)}")

# 打印总结
print(f"\n修复完成!")
print(f"成功修复: {fixed_files} 个文件")
print(f"修复失败: {failed_files} 个文件")