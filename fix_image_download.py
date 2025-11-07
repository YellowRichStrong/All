#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量修复图片工具页面中的下载功能
此脚本会扫描tools目录下的所有HTML文件，并修复图片下载按钮的点击事件处理逻辑
"""

import os
import re
import sys

def fix_download_functionality(file_path):
    """修复单个HTML文件中的图片下载功能"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文件是否包含下载按钮
        if 'downloadBtn' not in content:
            print(f"跳过 {os.path.basename(file_path)}: 未找到下载按钮")
            return False
        
        # 检查是否已经有下载事件监听器
        if 'downloadBtn.addEventListener' in content:
            # 提取按钮ID和文件名
            filename = os.path.basename(file_path).replace('.html', '')
            default_filename = f'{filename.replace("-", "-")}.png'
            
            # 替换现有的事件监听器
            pattern = r'downloadBtn\.addEventListener\([\s\S]*?\}\);'
            replacement = f'''downloadBtn.addEventListener('click', function(e) {{
                e.preventDefault(); // 防止a标签的默认行为
                
                if (!this.href) {{
                    Utils.showNotification('No image available to download', 'error');
                    return;
                }}
                
                // 创建临时下载链接以确保下载正常工作
                const tempLink = document.createElement('a');
                tempLink.href = this.href;
                tempLink.download = this.download || '{default_filename}';
                tempLink.style.display = 'none';
                
                document.body.appendChild(tempLink);
                tempLink.click();
                
                // 清理
                setTimeout(() => {{
                    document.body.removeChild(tempLink);
                }}, 100);
            }});'''
            
            # 替换已有的事件监听器
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        else:
            # 添加新的事件监听器到DOMContentLoaded函数末尾
            dom_content_loaded_pattern = r'document\.addEventListener\(["\']DOMContentLoaded["\'], function\(\)\s*\{{[\s\S]*?\}\);'
            match = re.search(dom_content_loaded_pattern, content)
            
            if match:
                dom_content = match.group(0)
                filename = os.path.basename(file_path).replace('.html', '')
                default_filename = f'{filename.replace("-", "-")}.png'
                
                new_event_listener = f'''
            // 修复下载按钮的点击事件
            downloadBtn.addEventListener('click', function(e) {{
                e.preventDefault(); // 防止a标签的默认行为
                
                if (!this.href) {{
                    Utils.showNotification('No image available to download', 'error');
                    return;
                }}
                
                // 创建临时下载链接以确保下载正常工作
                const tempLink = document.createElement('a');
                tempLink.href = this.href;
                tempLink.download = this.download || '{default_filename}';
                tempLink.style.display = 'none';
                
                document.body.appendChild(tempLink);
                tempLink.click();
                
                // 清理
                setTimeout(() => {{
                    document.body.removeChild(tempLink);
                }}, 100);
            }});'''
                
                # 在DOMContentLoaded函数末尾添加新的事件监听器
                updated_dom_content = dom_content.replace('        }});', f'{new_event_listener}\n        }});')
                content = content.replace(dom_content, updated_dom_content)
            else:
                print(f"警告: 在 {os.path.basename(file_path)} 中未找到DOMContentLoaded事件")
                return False
        
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已修复 {os.path.basename(file_path)} 的下载功能")
        return True
        
    except Exception as e:
        print(f"修复 {file_path} 时出错: {str(e)}")
        return False

def main():
    """主函数"""
    # 工具目录路径
    tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
    
    if not os.path.exists(tools_dir):
        print(f"错误: 工具目录不存在: {tools_dir}")
        sys.exit(1)
    
    # 获取所有HTML文件
    html_files = [f for f in os.listdir(tools_dir) if f.endswith('.html')]
    
    # 修复每个文件
    fixed_count = 0
    total_count = len(html_files)
    
    print(f"开始修复 {total_count} 个HTML文件中的下载功能...")
    
    for html_file in html_files:
        file_path = os.path.join(tools_dir, html_file)
        if fix_download_functionality(file_path):
            fixed_count += 1
    
    print(f"修复完成: 共 {fixed_count}/{total_count} 个文件")

if __name__ == "__main__":
    main()