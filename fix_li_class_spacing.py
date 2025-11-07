#!/usr/bin/env python3
import os
import re

def fix_li_class_spacing():
    """
    修复所有HTML文件中<li>标签和class属性之间缺少空格的问题
    将<liclass="active">替换为<li class="active">
    """
    tools_dir = "./tools"
    fixed_files = 0
    
    # 遍历tools目录下的所有HTML文件
    for filename in os.listdir(tools_dir):
        if filename.endswith(".html"):
            file_path = os.path.join(tools_dir, filename)
            
            # 读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否包含错误的模式
                if 'liclass="active"' in content:
                    # 替换错误模式
                    new_content = content.replace('liclass="active"', 'li class="active"')
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    fixed_files += 1
                    print(f"已修复: {filename}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")
    
    print(f"\n修复完成！共修复了 {fixed_files} 个文件。")

if __name__ == "__main__":
    fix_li_class_spacing()