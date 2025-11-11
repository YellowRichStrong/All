import os
import re

# 定义blog目录路径
blog_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/blog'

# 遍历blog目录下的所有HTML文件
for filename in os.listdir(blog_dir):
    if filename.endswith('.html') and filename != 'index.html':
        file_path = os.path.join(blog_dir, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 查找重复的面包屑导航
        breadcrumb_pattern = r'<!-- Breadcrumb -->\s*<div class="container">.*?</div>\s*</div>'
        breadcrumbs = re.findall(breadcrumb_pattern, content, re.DOTALL)
        
        # 如果找到多个面包屑导航，只保留第一个
        if len(breadcrumbs) > 1:
            # 替换所有面包屑导航为第一个
            first_breadcrumb = breadcrumbs[0]
            updated_content = re.sub(breadcrumb_pattern, '', content, flags=re.DOTALL)
            # 在header后添加第一个面包屑导航
            header_pattern = r'(</header>\s*)'
            updated_content = re.sub(header_pattern, f'\\1\n    {first_breadcrumb}\n', updated_content, flags=re.DOTALL)
            
            # 保存更新后的文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f'Fixed duplicate breadcrumbs in {filename}')

print('All duplicate breadcrumbs have been fixed!')