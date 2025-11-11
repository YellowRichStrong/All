import os
import re

# 定义目录路径
blog_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/blog'

# 修复重复面包屑导航的函数
def fix_duplicate_breadcrumbs(content):
    # 查找重复的面包屑导航
    breadcrumb_pattern = r'<!-- Breadcrumb -->\s*<div class="container">\s*<div class="breadcrumb">.*?</div>\s*</div>'
    breadcrumbs = re.findall(breadcrumb_pattern, content, re.DOTALL)
    
    # 如果找到多个面包屑导航，只保留第一个
    if len(breadcrumbs) > 1:
        # 保留第一个面包屑导航
        first_breadcrumb = breadcrumbs[0]
        
        # 删除所有面包屑导航
        content = re.sub(breadcrumb_pattern, '', content, flags=re.DOTALL)
        
        # 在header后添加第一个面包屑导航
        header_end_pattern = r'(</header>\s*)'
        replacement = f'\\1\n    {first_breadcrumb}\n'
        content = re.sub(header_end_pattern, replacement, content, flags=re.DOTALL)
    
    return content

# 清理旧CSS样式的函数
def clean_old_css(content):
    # 删除旧的导航CSS样式
    old_nav_css_patterns = [
        r'\s*\.logo a \{[^}]*\}\s*\n\s*\.nav-links \{[^}]*\}\s*\n\s*\.nav-links a \{[^}]*\}\s*\n\s*\.nav-links a:hover \{[^}]*\}\s*\n',
        r'\s*\.navbar \{[^}]*\}\s*\n\s*\.navbar \.container \{[^}]*\}\s*\n\s*\.logo a \{[^}]*\}\s*\n\s*\.nav-links \{[^}]*\}\s*\n\s*\.nav-links a \{[^}]*\}\s*\n\s*\.nav-links a:hover \{[^}]*\}\s*\n'
    ]
    
    for pattern in old_nav_css_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    return content

# 处理所有blog页面
print("修复Blog页面:")
for filename in os.listdir(blog_dir):
    if filename.endswith('.html') and filename != 'index.html':
        file_path = os.path.join(blog_dir, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 修复重复的面包屑导航
        content = fix_duplicate_breadcrumbs(content)
        
        # 清理旧的CSS样式
        content = clean_old_css(content)
        
        # 保存更新后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"  已修复 {filename}")

print("\n所有页面修复完成!")