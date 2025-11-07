#!/usr/bin/env python3
import os
import re

# 需要处理的HTML文件
root_html_files = ['index.html', 'encry.html', 'code.html', 'network.html', 'dav.html', 'text.html', 'contact.html', 'privacy.html', 'terms.html']

# 获取tools目录下所有HTML文件
def get_tools_html_files():
    tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
    html_files = []
    if os.path.exists(tools_dir):
        for file in os.listdir(tools_dir):
            if file.endswith('.html'):
                html_files.append(os.path.join(tools_dir, file))
    return html_files

def update_navigation(file_path):
    """更新导航栏，确保包含Text Tools菜单项"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取文件名用于日志
        filename = os.path.basename(file_path)
        
        # 检查是否已包含Text Tools菜单项
        if 'href="../text.html">Text Tools</a>' in content or 'href="text.html">Text Tools</a>' in content:
            print(f"跳过: {filename} 已包含Text Tools菜单项")
            return "skipped"
        
        # 定义导航栏搜索模式（更宽松的正则表达式）
        nav_pattern = re.compile(r'<nav>.*?<ul>.*?</ul>.*?</nav>', re.DOTALL)
        
        # 尝试匹配导航栏
        match = nav_pattern.search(content)
        if match:
            nav_content = match.group(0)
            
            # 检查相对路径
            relative_path = '../' if 'tools/' in file_path else ''
            
            # 创建Text Tools菜单项
            text_tools_item = f'<li><a href="{relative_path}text.html">Text Tools</a></li>'
            
            # 尝试在Network Tools后插入
            if 'Network Tools' in nav_content:
                new_nav_content = re.sub(r'(<li><a href="' + re.escape(relative_path) + r'network.html">Network Tools</a></li>)', r'\1\n                        ' + text_tools_item, nav_content)
            # 或者在Code Tools后插入
            elif 'Code Tools' in nav_content:
                new_nav_content = re.sub(r'(<li><a href="' + re.escape(relative_path) + r'code.html".*?>Code Tools</a></li>)', r'\1\n                        ' + text_tools_item, nav_content)
            # 或者在Encry Tools后插入
            elif 'Encry Tools' in nav_content:
                new_nav_content = re.sub(r'(<li><a href="' + re.escape(relative_path) + r'encry.html">Encry Tools</a></li>)', r'\1\n                        ' + text_tools_item, nav_content)
            # 或者在Image Tools后插入
            elif 'Image Tools' in nav_content:
                new_nav_content = re.sub(r'(<li><a href="' + re.escape(relative_path) + r'index.html">Image Tools</a></li>)', r'\1\n                        ' + text_tools_item, nav_content)
            else:
                # 如果找不到特定菜单项，在ul标签内的最后一个li前插入
                if '<li' in nav_content and '</ul>' in nav_content:
                    parts = nav_content.split('</ul>')
                    if '<li' in parts[0]:
                        li_items = parts[0].split('<li')
                        # 在最后一个li标签前插入
                        modified_li_items = []
                        for i, li in enumerate(li_items):
                            modified_li_items.append(li)
                            if i == len(li_items) - 2:  # 在倒数第二个li后插入
                                modified_li_items.append(text_tools_item)
                        parts[0] = '<li'.join(modified_li_items)
                        new_nav_content = '</ul>'.join(parts)
                    else:
                        # 如果ul内没有li，直接添加
                        new_nav_content = parts[0] + '                        ' + text_tools_item + '\n                    </ul>'.join(parts[1:])
                else:
                    print(f"警告: 无法更新 {filename} 的导航栏，找不到合适的位置")
                    return "failed"
            
            # 写回文件
            new_content = content.replace(nav_content, new_nav_content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"已更新: {filename}")
            return "updated"
        else:
            # 如果没找到标准导航栏模式，尝试查找<ul>标签内的导航项
            ul_pattern = re.compile(r'<ul>.*?</ul>', re.DOTALL)
            ul_match = ul_pattern.search(content)
            if ul_match:
                ul_content = ul_match.group(0)
                
                # 检查是否包含导航项
                if 'href="' in ul_content and ('Image Tools' in ul_content or 'Encry Tools' in ul_content):
                    # 检查相对路径
                    relative_path = '../' if 'tools/' in file_path else ''
                    
                    # 创建Text Tools菜单项
                    text_tools_item = f'<li><a href="{relative_path}text.html">Text Tools</a></li>'
                    
                    # 尝试在适当位置插入
                    if 'Network Tools' in ul_content:
                        new_ul_content = re.sub(r'(<li><a href="' + re.escape(relative_path) + r'network.html">Network Tools</a></li>)', r'\1\n                        ' + text_tools_item, ul_content)
                    elif 'Code Tools' in ul_content:
                        new_ul_content = re.sub(r'(<li><a href="' + re.escape(relative_path) + r'code.html".*?>Code Tools</a></li>)', r'\1\n                        ' + text_tools_item, ul_content)
                    elif 'Encry Tools' in ul_content:
                        new_ul_content = re.sub(r'(<li><a href="' + re.escape(relative_path) + r'encry.html">Encry Tools</a></li>)', r'\1\n                        ' + text_tools_item, ul_content)
                    elif 'Image Tools' in ul_content:
                        new_ul_content = re.sub(r'(<li><a href="' + re.escape(relative_path) + r'index.html">Image Tools</a></li>)', r'\1\n                        ' + text_tools_item, ul_content)
                    else:
                        # 在ul标签内的最后一个li前插入
                        if '<li' in ul_content and '</ul>' in ul_content:
                            parts = ul_content.split('</ul>')
                            if '<li' in parts[0]:
                                li_items = parts[0].split('<li')
                                modified_li_items = []
                                for i, li in enumerate(li_items):
                                    modified_li_items.append(li)
                                    if i == len(li_items) - 2:
                                        modified_li_items.append(text_tools_item)
                                parts[0] = '<li'.join(modified_li_items)
                                new_ul_content = '</ul>'.join(parts)
                            else:
                                new_ul_content = parts[0] + '                        ' + text_tools_item + '\n                    </ul>'.join(parts[1:])
                        else:
                            print(f"警告: 无法更新 {filename} 的导航栏，找不到合适的位置")
                            return "failed"
                    
                    # 写回文件
                    new_content = content.replace(ul_content, new_ul_content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"已更新: {filename}")
                    return "updated"
                else:
                    return "failed"
            
            print(f"警告: 无法在 {filename} 中找到导航栏结构")
            return "failed"
            
    except Exception as e:
        print(f"处理文件 {filename} 时出错: {str(e)}")
        return "failed"

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("开始更新所有文件中的导航栏，添加Text Tools链接...")
    
    # 获取所有需要处理的HTML文件
    all_html_files = [os.path.join(script_dir, file) for file in root_html_files] + get_tools_html_files()
    print(f"共找到 {len(all_html_files)} 个HTML文件需要处理")
    
    # 处理所有HTML文件
    total_updated = 0
    skipped_count = 0
    failed_count = 0
    
    for html_file in all_html_files:
        if os.path.exists(html_file):
            result = update_navigation(html_file)
            if result == "updated":
                total_updated += 1
            elif result == "skipped":
                skipped_count += 1
            else:
                failed_count += 1
        else:
            print(f"警告: 文件不存在 {os.path.basename(html_file)}")
            failed_count += 1
    
    print(f"\n处理完成!")
    print(f"更新成功: {total_updated} 个文件")
    print(f"跳过: {skipped_count} 个文件（已包含Text Tools菜单项）")
    print(f"失败: {failed_count} 个文件")

if __name__ == "__main__":
    main()