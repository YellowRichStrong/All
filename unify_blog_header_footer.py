#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一博客页面头部和底部样式脚本
将所有blog/*.html的header和footer替换为与index.html一致的样式
"""

import os
import re
from pathlib import Path

# 标准的header模板（与index.html一致）
STANDARD_HEADER = '''    <!-- Header -->
    <header>
        <div class="container">
            <div class="logo">
                <a href="../index.html">
                    <img src="../images/logo.png" alt="OOPEN AII Logo">
                </a>
                <h1>OOPEN AII</h1>
            </div>
            <nav>
                <ul>
                    <li><a href="../index.html">Image Tools</a></li>
                    <li><a href="../encry.html">Encry Tools</a></li>
                    <li><a href="../code.html" style="display:block !important;">Code Tools</a></li>
                    <li><a href="../network.html">Network Tools</a></li>
                    <li><a href="../text.html">Text Tools</a></li>
                    <li><a href="../dav.html">Dav</a></li>
                </ul>
            </nav>
        </div>
    </header>'''

# 标准的footer模板（与index.html一致）
STANDARD_FOOTER = '''    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-info">
                    <h3>OOPEN AII</h3>
                    <p>Providing powerful image tools for all your needs. All tools are free to use and work entirely in your browser.</p>
                </div>
                <div>
                    <h3>Quick Links</h3>
                    <div class="footer-links">
                        <a href="../index.html">Home</a>
                        <a href="../blog/index.html">Blog</a>
                        <a href="../contact.html">Contact Us</a>
                        <a href="../privacy.html">Privacy Policy</a>
                        <a href="../terms.html">User Rights</a>
                    </div>
                </div>
            </div>
            <div class="copyright">
                <p>© 2026 OOPEN AII. All rights reserved.</p>
                <p>Contact: tankeapp@gmail.com</p>
            </div>
        </div>
    </footer>

    <!-- Back to Top Button -->
    <button id="backToTop" class="back-to-top">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"></path></svg>
    </button>

    <script src="../js/main.js"></script>'''

def replace_header_footer(file_path):
    """替换单个文件的header和footer"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 替换header部分 - 匹配从<!-- Header -->到</header>
        header_pattern = r'(\s*<!-- Header -->.*?</header>)'
        content = re.sub(header_pattern, '\n' + STANDARD_HEADER + '\n', content, flags=re.DOTALL)
        
        # 替换footer部分 - 匹配从<!-- Footer -->到</body>之前
        footer_pattern = r'(\s*<!-- Footer -->.*?)(</body>)'
        content = re.sub(footer_pattern, '\n' + STANDARD_FOOTER + '\n\\2', content, flags=re.DOTALL)
        
        # 只有内容发生变化时才写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"❌ 处理文件 {file_path} 时出错: {e}")
        return False

def main():
    print("=" * 60)
    print("统一博客页面头部和底部样式")
    print("=" * 60)
    
    # 获取blog目录
    blog_dir = Path('blog')
    if not blog_dir.exists():
        print("❌ blog目录不存在")
        return
    
    # 获取所有HTML文件（排除index.html）
    html_files = [f for f in blog_dir.glob('*.html') if f.name != 'index.html']
    
    print(f"\n找到 {len(html_files)} 个博客文章文件\n")
    
    updated_count = 0
    skipped_count = 0
    
    for html_file in html_files:
        file_name = html_file.name
        print(f"处理: {file_name}...", end=' ')
        
        if replace_header_footer(html_file):
            print("✅ 已更新")
            updated_count += 1
        else:
            print("⏭️  跳过（无需更新）")
            skipped_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 统一完成！")
    print(f"   更新文件数: {updated_count}")
    print(f"   跳过文件数: {skipped_count}")
    print(f"   总文件数: {len(html_files)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
