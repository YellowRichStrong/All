import os
import re

# 定义目录路径
blog_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/blog'

# 清理旧CSS样式的函数
def clean_old_navigation_css(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 查找并删除旧的导航CSS样式
    # 匹配从.navbar开始到下一个CSS规则或文件结尾的模式
    navbar_pattern = r'\s*\.navbar\s*\{[^}]*\}[^}]*\.navbar\s*\.container\s*\{[^}]*\}[^}]*\.logo\s*a\s*\{[^}]*\}[^}]*\.nav-links\s*\{[^}]*\}[^}]*\.nav-links\s*a\s*\{[^}]*\}[^}]*\.nav-links\s*a:hover\s*\{[^}]*\}'
    
    # 使用更简单的模式匹配
    old_css_patterns = [
        r'\s*\.navbar\s*\{.*?\}\s*\n\s*\.navbar\s*\.container\s*\{.*?\}\s*\n\s*\.logo\s*a\s*\{.*?\}\s*\n\s*\.nav-links\s*\{.*?\}\s*\n\s*\.nav-links\s*a\s*\{.*?\}\s*\n\s*\.nav-links\s*a:hover\s*\{.*?\}\s*\n',
        r'\s*\.logo\s*a\s*\{.*?\}\s*\n\s*\.nav-links\s*\{.*?\}\s*\n\s*\.nav-links\s*a\s*\{.*?\}\s*\n\s*\.nav-links\s*a:hover\s*\{.*?\}\s*\n'
    ]
    
    modified = False
    for pattern in old_css_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"已清理旧CSS样式: {os.path.basename(file_path)}")

# 处理所有blog页面
print("清理旧的导航CSS样式:")
for filename in os.listdir(blog_dir):
    if filename.endswith('.html') and filename != 'index.html':
        file_path = os.path.join(blog_dir, filename)
        clean_old_navigation_css(file_path)

print("\n清理完成!")