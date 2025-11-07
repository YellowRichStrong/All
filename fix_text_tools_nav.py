import os
import re

# 定义tools目录路径
tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'

# 预期的菜单项顺序
expected_menu_order = [
    ('Image Tools', '../index.html'),
    ('Encry Tools', '../encry.html'),
    ('Code Tools', '../code.html'),
    ('Network Tools', '../network.html'),
    ('Text Tools', '../text.html'),
    ('Dav', '../dav.html')
]

def fix_navigation(file_path):
    """检查并修复HTML文件中的导航栏结构"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找导航栏中的ul列表
        nav_pattern = re.compile(r'(<nav>[\s\S]*?<ul>)([\s\S]*?)(</ul>[\s\S]*?</nav>)')
        match = nav_pattern.search(content)
        
        if not match:
            print(f"警告: 在 {os.path.basename(file_path)} 中未找到导航栏结构")
            return False
        
        before_ul = match.group(1)
        ul_content = match.group(2)
        after_ul = match.group(3)
        
        # 检查是否包含Text Tools菜单项
        has_text_tools = '<li><a href="../text.html">Text Tools</a></li>' in ul_content
        
        # 创建新的导航项列表
        new_nav_items = []
        for text, link in expected_menu_order:
            # 检查是否有活动项
            active_class = 'class="active" ' if f'<li class="active"><a href="{link}"' in ul_content else ''
            
            # 处理特殊情况，如Code Tools的display:block样式
            special_style = ' style="display:block !important;"' if text == 'Code Tools' else ''
            
            new_nav_items.append(f'                        <li{active_class}><a href="{link}"{special_style}>{text}</a></li>')
        
        # 构建新的ul内容
        new_ul_content = '\n'.join(new_nav_items)
        
        # 更新文件内容
        new_content = content.replace(before_ul + ul_content + after_ul, 
                                      before_ul + '\n' + new_ul_content + '\n                    ' + after_ul)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        status = "修复了顺序" if has_text_tools else "添加了Text Tools"
        print(f"已更新 {os.path.basename(file_path)}: {status}")
        return True
        
    except Exception as e:
        print(f"处理 {os.path.basename(file_path)} 时出错: {str(e)}")
        return False

def main():
    """主函数，遍历并处理所有HTML文件"""
    success_count = 0
    fail_count = 0
    
    # 获取所有HTML文件
    html_files = [f for f in os.listdir(tools_dir) if f.endswith('.html')]
    
    print(f"找到 {len(html_files)} 个HTML文件，开始处理...")
    
    for html_file in html_files:
        file_path = os.path.join(tools_dir, html_file)
        if fix_navigation(file_path):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"处理完成: 成功 {success_count} 个，失败 {fail_count} 个")

if __name__ == "__main__":
    main()