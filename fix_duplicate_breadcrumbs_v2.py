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
            # 找到第一个面包屑导航的位置
            first_match = re.search(breadcrumb_pattern, content, re.DOTALL)
            if first_match:
                first_breadcrumb = first_match.group(0)
                
                # 删除所有面包屑导航
                updated_content = re.sub(breadcrumb_pattern, '', content, flags=re.DOTALL)
                
                # 在header后添加第一个面包屑导航
                header_end_pattern = r'(</header>\s*)'
                replacement = f'\\1\n    {first_breadcrumb}\n'
                updated_content = re.sub(header_end_pattern, replacement, updated_content, flags=re.DOTALL)
                
                # 保存更新后的文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
                
                print(f'Fixed duplicate breadcrumbs in {filename}')

print('All duplicate breadcrumbs have been fixed!')