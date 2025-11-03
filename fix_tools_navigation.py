import os
import re

# 定义tools目录路径
tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'

# 遍历tools目录下的所有HTML文件
for filename in os.listdir(tools_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(tools_dir, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 定义导航栏的正则表达式模式
        nav_pattern = r'<nav>\s*<ul>\s*<li[^>]*><a[^>]*href="\.\./index\.html"[^>]*>Image Tools</a></li>\s*(.*?)\s*</ul>\s*</nav>'
        
        # 查找导航栏
        match = re.search(nav_pattern, content, re.DOTALL)
        if match:
            # 提取导航栏中的中间内容
            nav_content = match.group(1)
            
            # 检查是否已经包含Encry Tools
            has_encry_tools = 'Encry Tools' in nav_content or 'Encry</a>' in nav_content
            # 检查是否已经包含Code Tools
            has_code_tools = 'Code Tools' in nav_content
            
            # 确定当前页面类型，设置active类
            is_image_tool = filename in ['text-to-image.html', 'image-color-extraction.html', 'image-watermark.html', 'placeholder-generator.html', 
                                       'image-grid-cutter.html', 'image-mosaic.html', 'base64-to-image.html', 'image-to-excel.html', 
                                       'screen-color-picker.html', 'image-to-grayscale.html', 'image-compressor.html', 'image-rounded-corners.html', 
                                       'maze-generator.html', 'image-converter.html', 'image-cropper.html', 'icon-changer.html', 
                                       'image-add-text.html', 'favicon-generator.html', 'icon-to-base64.html', 'image-stitching.html']
            
            is_encry_tool = filename.endswith('-encryption.html') or filename in ['jwt-encryption.html', 'sha-encryption.html']
            is_code_tool = filename in ['css-minify-format.html', 'html-minify-format.html', 'js-minify-format.html', 'xml-minify-format.html']
            is_network_tool = filename in ['ip-lookup.html', 'ping-test.html', 'dns-lookup.html', 'ip-to-domain.html', 'port-scanner.html', 
                                         'traceroute.html', 'network-speed-test.html', 'http-headers.html', 'ssl-checker.html', 
                                         'website-performance.html', 'website-uptime.html', 'whois-lookup.html']
            is_dav_tool = filename in ['color-converter.html', 'data-size-converter.html', 'pinyin-converter.html', 'json-compressor.html', 
                                     'sql-minify-format.html', 'base-converter.html', 'url-encoder.html', 'regex-tester.html', 
                                     'text-binary-converter.html', 'json-get-converter.html', 'base64-encoder.html', 'html-preview.html', 
                                     'json-formatter.html', 'timestamp-converter.html', 'string-comparison.html', 'time-diff-calculator.html', 
                                     'word-counter.html', 'ascii-converter.html', 'js-debugger.html', 'xml-json-converter.html']
            
            # 构建新的导航栏内容
            new_nav_content = ''
            
            # Image Tools链接
            if is_image_tool:
                new_nav_content += '                    <li class="active"><a href="../index.html">Image Tools</a></li>\n'
            else:
                new_nav_content += '                    <li><a href="../index.html">Image Tools</a></li>\n'
            
            # Encry Tools链接
            if is_encry_tool:
                new_nav_content += '                    <li class="active"><a href="../encry.html">Encry Tools</a></li>\n'
            else:
                new_nav_content += '                    <li><a href="../encry.html">Encry Tools</a></li>\n'
            
            # Code Tools链接
            new_nav_content += '                    <li><a href="../code.html" style="display:block !important;">Code Tools</a></li>\n'
            
            # Network Tools链接
            if is_network_tool:
                new_nav_content += '                    <li class="active"><a href="../network.html">Network Tools</a></li>\n'
            else:
                new_nav_content += '                    <li><a href="../network.html">Network Tools</a></li>\n'
            
            # Dav链接
            if is_dav_tool and not is_network_tool:
                new_nav_content += '                    <li class="active"><a href="../dav.html">Dav</a></li>\n'
            else:
                new_nav_content += '                    <li><a href="../dav.html">Dav</a></li>\n'
            
            # 替换导航栏
            new_nav = f'<nav>\n                <ul>\n{new_nav_content}                </ul>\n            </nav>'
            updated_content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)
            
            # 保存更新后的文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f'Fixed navigation in {filename}')

print('All tool pages navigation bars have been updated!')