#!/usr/bin/env python3
import os
import re

# 设置要修复的目录
directory = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'

# 修复的计数器
fixed_files = 0
failed_files = 0

# 遍历目录中的所有HTML文件
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否需要修复（检查面包屑导航中是否有"Code Tools"）
                if '<li><a href="../code.html">Code Tools</a></li>' in content:
                    # 修复第一种格式：使用ul/li标签的格式
                    new_content = content.replace('<li><a href="../code.html">Code Tools</a></li>', '<li><a href="../dav.html">Dav</a></li>')
                    
                    # 修复第二种格式：直接的链接格式（如果存在）
                    if '<a href="../code.html">Code Tools</a> &gt;' in new_content:
                        new_content = new_content.replace('<a href="../code.html">Code Tools</a> &gt;', '<a href="../dav.html">Dav</a> &gt;')
                    
                    # 保存修复后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"已修复文件: {file_path}")
                    fixed_files += 1
                else:
                    # 检查是否有第二种格式需要修复
                    if '<a href="../code.html">Code Tools</a> &gt;' in content:
                        new_content = content.replace('<a href="../code.html">Code Tools</a> &gt;', '<a href="../dav.html">Dav</a> &gt;')
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"已修复文件（仅修复第二种格式）: {file_path}")
                        fixed_files += 1
            except Exception as e:
                print(f"修复文件失败 {file_path}: {e}")
                failed_files += 1

# 打印修复统计信息
print(f"\n修复完成！")
print(f"成功修复: {fixed_files} 个文件")
print(f"修复失败: {failed_files} 个文件")