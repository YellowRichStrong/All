import os
import re

# 工具目录路径
tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'

# 统计修复情况
fixed_files = 0
processed_files = 0

# 工具页面类型映射
TOOL_TYPES = {
    # 图片工具
    'image': [
        'text-to-image', 'image-compressor', 'image-watermark', 'image-to-text', 'resize-image', 'favicon-generator',
        'image-cropper', 'image-converter', 'image-grid-cutter', 'image-mosaic', 'image-rounded-corners', 
        'image-stitching', 'image-to-excel', 'image-to-grayscale', 'image-add-text', 'image-color-extraction',
        'icon-changer', 'icon-to-base64', 'base64-to-image'
    ],
    # 加密工具
    'encry': [
        'aes-encryption', 'jwt-encryption', 'rc4-encryption', 'rsa-encryption', 'base64-encoder-decoder', 
        'md5-generator', 'sha256-generator', 'md5-encryption', 'sha-encryption', 'shake-encryption',
        'rabbit-encryption', 'rc4-encryption', 'tripledes-encryption', 'des-encryption', 'hmac-hash-encryption',
        'ripemd160-encryption', 'keccak-encryption', 'js-eval-encryption', 'crc32-encryption', 'base64-encoder'
    ],
    # 代码工具
    'code': [
        'css-minify-format', 'js-minify-format', 'html-minify-format', 'json-formatter', 'xml-formatter', 
        'sql-minify-format', 'color-converter', 'json-compressor', 'json-get-converter', 'xml-json-converter',
        'xml-minify-format', 'html-preview', 'js-debugger', 'regex-tester', 'color-picker'
    ]
}

# 遍历tools目录下所有HTML文件
for filename in os.listdir(tools_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(tools_dir, filename)
        processed_files += 1
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有面包屑导航
        if '<div class="breadcrumb">' in content:
            # 检查是否需要修改现有面包屑导航（英文转中文）
            if 'Home' in content:
                content = content.replace('Home', 'index')
            if 'Encryption Tools' in content:
                content = content.replace('Encryption Tools', 'Encry Tools')
            
            # 保存修改
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'已更新现有面包屑导航: {filename}')
            fixed_files += 1
            continue
        
        # 确定工具类型和页面标题
        tool_name = filename.replace('.html', '')
        page_title = tool_name.replace('-', ' ').title()
        
        # 确定面包屑导航路径
        breadcrumb = ''
        if any(tool_name in tools for tools in TOOL_TYPES.values()):
            # 查找工具类型
            tool_type = None
            for type_key, tools_list in TOOL_TYPES.items():
                if tool_name in tools_list:
                    tool_type = type_key
                    break
            
            # 构建面包屑导航
            if tool_type == 'image':
                breadcrumb = '''            <div class="breadcrumb">
                <a href="../index.html">index</a> &gt; 
                <a href="../index.html">Image Tools</a> &gt; 
                <span>{}</span>
            </div>'''.format(page_title)
            elif tool_type == 'encry':
                breadcrumb = '''            <div class="breadcrumb">
                <a href="../index.html">index</a> &gt; 
                <a href="../encry.html">Encry Tools</a> &gt; 
                <span>{}</span>
            </div>'''.format(page_title)
            elif tool_type == 'code':
                breadcrumb = '''            <div class="breadcrumb">
                <a href="../index.html">index</a> &gt; 
                <a href="../code.html">Code Tools</a> &gt; 
                <span>{}</span>
            </div>'''.format(page_title)
        
        # 如果找到工具类型，添加面包屑导航
        if breadcrumb:
            # 查找main标签内的container或tool-container位置
            if '<main>\n        <div class="container">\n            <div class="tool-container">' in content:
                # 替换为带面包屑的结构
                content = content.replace(
                    '<main>\n        <div class="container">\n            <div class="tool-container">',
                    '<main>\n        <div class="container">\n{}\n            <div class="tool-container">'.format(breadcrumb)
                )
            elif '<main>\n        <div class="container">' in content:
                # 查找container后的第一个div
                content = content.replace(
                    '<main>\n        <div class="container">',
                    '<main>\n        <div class="container">\n{}\n'.format(breadcrumb)
                )
            elif '<main>\n        <div class="tool-container">' in content:
                # 直接在main后添加面包屑
                content = content.replace(
                    '<main>\n        <div class="tool-container">',
                    '<main>\n        <div class="container">\n{}\n        </div>\n        <div class="tool-container">'.format(breadcrumb)
                )
            
            # 保存修改
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'已添加面包屑导航: {filename}')
            fixed_files += 1
        else:
            print(f'未识别工具类型，跳过: {filename}')

print(f'\n修复完成！')
print(f'处理文件总数: {processed_files}')
print(f'成功修复文件数: {fixed_files}')