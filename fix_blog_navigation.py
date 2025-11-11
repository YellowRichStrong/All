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
        
        # 修复导航栏 - 替换自定义navbar为标准header
        old_nav_pattern = r'<!-- 导航栏 -->\s*<nav class="navbar">.*?</nav>'
        new_nav = '''    <!-- Header -->
    <header>
        <div class="container">
            <div class="logo">
                <a href="https://openai2026.com">
                    <img src="https://openai2026.com/images/logo.png" alt="OOPEN AII Logo">
                </a>
                <h1>OOPEN AII</h1>
            </div>
            <nav>
                <ul>
                    <li><a href="https://openai2026.com">Image Tools</a></li>
                    <li><a href="https://openai2026.com/encry.html">Encry Tools</a></li>
                    <li><a href="https://openai2026.com/code.html">Code Tools</a></li>
                    <li><a href="https://openai2026.com/network.html">Network Tools</a></li>
                    <li><a href="https://openai2026.com/text.html">Text Tools</a></li>
                    <li><a href="https://openai2026.com/dav.html">Dav</a></li>
                </ul>
            </nav>
        </div>
    </header>'''
        
        # 替换导航栏
        updated_content = re.sub(old_nav_pattern, new_nav, content, flags=re.DOTALL)
        
        # 修复面包屑导航 - 如果存在的话
        old_breadcrumb_pattern = r'<!-- 面包屑导航 -->\s*<div class="container">.*?</div>\s*</div>'
        new_breadcrumb = '''    <!-- Breadcrumb -->
    <div class="container">
        <div class="breadcrumb">
            <a href="https://openai2026.com">Home</a> &gt; 
            <a href="https://openai2026.com/blog/index.html">Blog</a> &gt; 
            <span>{}</span>
        </div>
    </div>'''.format(filename.replace('.html', '').replace('-', ' ').title())
        
        # 替换面包屑导航
        updated_content = re.sub(old_breadcrumb_pattern, new_breadcrumb, updated_content, flags=re.DOTALL)
        
        # 处理没有面包屑导航的情况
        if '<!-- 面包屑导航 -->' not in updated_content and '<div class="breadcrumb">' not in updated_content:
            # 在header后添加面包屑导航
            header_pattern = r'(</header>\s*)'
            breadcrumb_insert = '''</header>
    
    <!-- Breadcrumb -->
    <div class="container">
        <div class="breadcrumb">
            <a href="https://openai2026.com">Home</a> &gt; 
            <a href="https://openai2026.com/blog/index.html">Blog</a> &gt; 
            <span>{}</span>
        </div>
    </div>'''.format(filename.replace('.html', '').replace('-', ' ').title())
            
            updated_content = re.sub(header_pattern, breadcrumb_insert, updated_content, flags=re.DOTALL)
        
        # 保存更新后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f'Fixed navigation in {filename}')

print('All blog pages navigation bars and breadcrumbs have been updated!')