import os
import re

# 获取text.html中列出的所有工具链接
def get_tools_from_html():
    html_path = '/Users/macbookpro/Desktop/trae/oopenai2026/text.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取所有工具链接
    tool_links = re.findall(r'<a href="tools/(.*?)" class="tool-card-link">', html_content)
    return tool_links

# 获取tools目录中实际存在的文件
def get_existing_tools():
    tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'
    return set(os.listdir(tools_dir))

# 检查缺失的工具
def check_missing_tools():
    html_tools = get_tools_from_html()
    existing_tools = get_existing_tools()
    
    print("检查文本工具文件是否存在：")
    print(f"text.html中列出的工具数量: {len(html_tools)}")
    print(f"tools目录中存在的文件数量: {len(existing_tools)}")
    print("\n缺失的工具文件:")
    
    missing_tools = []
    for tool in html_tools:
        if tool not in existing_tools:
            missing_tools.append(tool)
            print(f"- {tool}")
    
    print(f"\n缺失的工具总数: {len(missing_tools)}")
    
    # 检查是否有未在text.html中列出但实际存在的文本工具
    text_tools = [t for t in existing_tools if t.startswith('text-') or t.startswith('word-') or t.startswith('line-') or t.startswith('case-') or t == 'lorem-ipsum-generator.html']
    unlisted_tools = [t for t in text_tools if t not in html_tools]
    
    print("\n未在text.html中列出但实际存在的文本工具:")
    for tool in unlisted_tools:
        print(f"- {tool}")
    
    print(f"\n未列出的文本工具总数: {len(unlisted_tools)}")

if __name__ == "__main__":
    check_missing_tools()