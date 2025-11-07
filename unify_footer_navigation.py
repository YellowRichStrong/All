#!/usr/bin/env python3
import os
import re

# 读取index.html中的footer结构作为模板
def get_footer_template():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # 提取footer部分
    footer_match = re.search(r'<footer>.*?</footer>', content, re.DOTALL)
    if footer_match:
        return footer_match.group(0)
    return None

# 为不同目录的文件调整footer中的链接路径
def adjust_links(footer_content, file_path):
    # 如果是tools目录下的文件，需要调整链接路径为上一级
    if 'tools/' in file_path:
        # 将href="index.html" 改为 href="../index.html"
        footer_content = re.sub(r'href="(index|contact|privacy|terms)\.html"', r'href="../\1.html"', footer_content)
    return footer_content

# 替换文件中的footer结构
def replace_footer(file_path, footer_template):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 调整链接路径
        adjusted_footer = adjust_links(footer_template, file_path)
        
        # 替换footer部分
        if re.search(r'<footer>.*?</footer>', content, re.DOTALL):
            new_content = re.sub(r'<footer>.*?</footer>', adjusted_footer, content, flags=re.DOTALL)
        else:
            # 如果没有footer，在</body>前添加
            if '</body>' in content:
                new_content = content.replace('</body>', f'{adjusted_footer}\n</body>')
            else:
                print(f"警告: {file_path} 中没有找到 </body> 标签")
                return False
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

# 主函数
def main():
    # 获取footer模板
    footer_template = get_footer_template()
    if not footer_template:
        print("错误: 无法从index.html中提取footer结构")
        return
    
    # 获取所有HTML文件
    html_files = []
    
    # 主目录下的HTML文件
    for file in os.listdir('.'):
        if file.endswith('.html') and file != 'index.html':  # 跳过index.html本身
            html_files.append(file)
    
    # tools目录下的HTML文件
    tools_dir = 'tools'
    if os.path.exists(tools_dir):
        for file in os.listdir(tools_dir):
            if file.endswith('.html'):
                html_files.append(os.path.join(tools_dir, file))
    
    # 处理每个HTML文件
    success_count = 0
    error_count = 0
    
    for file_path in html_files:
        print(f"处理文件: {file_path}")
        if replace_footer(file_path, footer_template):
            success_count += 1
        else:
            error_count += 1
    
    print(f"\n处理完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {error_count} 个文件")

if __name__ == "__main__":
    main()