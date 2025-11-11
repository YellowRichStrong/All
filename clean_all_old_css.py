import os
import re

# 定义目录路径
blog_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/blog'

# 清理所有旧CSS样式
def clean_all_old_css(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 查找并删除旧的导航CSS样式
    old_nav_css_pattern = r'\s*/\* 导航栏样式 \*/\s*.navbar \{.*?\}\s*.navbar \.container \{.*?\}\s*'
    
    if re.search(old_nav_css_pattern, content, re.DOTALL):
        content = re.sub(old_nav_css_pattern, '', content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"已清理旧CSS样式: {os.path.basename(file_path)}")

# 处理所有blog页面
print("清理所有旧的导航CSS样式:")
for filename in os.listdir(blog_dir):
    if filename.endswith('.html') and filename != 'index.html':
        file_path = os.path.join(blog_dir, filename)
        clean_all_old_css(file_path)

print("\n清理完成!")