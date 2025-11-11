import os
import re

# 定义目录路径
blog_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/blog'
tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'

# 检查函数
def check_navigation_consistency(file_path, file_type):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    issues = []
    
    # 检查是否使用标准header导航
    if '<header>' not in content and '<nav class="navbar">' in content:
        issues.append("使用了旧的navbar样式而不是标准header")
    
    # 检查面包屑导航
    breadcrumb_pattern = r'<!-- Breadcrumb -->\s*<div class="container">\s*<div class="breadcrumb">.*?</div>\s*</div>'
    breadcrumbs = re.findall(breadcrumb_pattern, content, re.DOTALL)
    if len(breadcrumbs) > 1:
        issues.append(f"发现{len(breadcrumbs)}个重复的面包屑导航")
    
    # 检查是否包含旧的CSS样式
    if '.nav-links {' in content or '.navbar {' in content:
        issues.append("包含旧的导航CSS样式")
    
    # 检查logo
    if '<img src="https://openai2026.com/images/logo.png"' not in content and '<img src="../images/logo.png"' not in content and '<img src="images/logo.png"' not in content:
        if file_type == "blog":
            issues.append("Logo路径可能不正确")
    
    return issues

# 检查blog页面
print("检查Blog页面:")
for filename in os.listdir(blog_dir):
    if filename.endswith('.html') and filename != 'index.html':
        file_path = os.path.join(blog_dir, filename)
        issues = check_navigation_consistency(file_path, "blog")
        if issues:
            print(f"  {filename}:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print(f"  {filename}: OK")

# 检查工具页面
print("\n检查工具页面:")
for filename in os.listdir(tools_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(tools_dir, filename)
        issues = check_navigation_consistency(file_path, "tool")
        if issues:
            print(f"  {filename}:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print(f"  {filename}: OK")

print("\n检查完成!")