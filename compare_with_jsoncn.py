# 基于搜索结果和常见的文本工具，列出json.cn可能提供的文本工具功能
import os

# json.cn可能提供的文本工具（基于搜索和常见工具）
jsoncn_possible_tools = [
    # 基础文本处理
    'binary-octal-converter.html',  # 从搜索结果中确认
    'hex-decimal-converter.html',   # 十六进制十进制转换
    'roman-numeral-converter.html', # 罗马数字转换
    'text-to-json.html',            # 文本转JSON
    'json-to-text.html',            # JSON转文本
    'csv-to-json.html',             # CSV转JSON
    'json-to-csv.html',             # JSON转CSV
    'html-escape-unescape.html',    # HTML转义/反转义
    'css-minify-format.html',       # CSS压缩格式化
    'js-minify-format.html',        # JS压缩格式化
    'sql-minify-format.html',       # SQL压缩格式化
    'xml-minify-format.html',       # XML压缩格式化
    
    # 文本分析和转换
    'text-to-image.html',           # 已存在但未列出
    'text-to-speech.html',          # 文本转语音
    'speech-to-text.html',          # 语音转文本
    'ocr-text-extractor.html',      # OCR文本提取
    'emoji-to-text.html',           # Emoji转文本
    'text-to-emoji.html',           # 文本转Emoji
    'text-translator.html',         # 文本翻译
    'text-summarizer.html',         # 文本摘要
    
    # 编码转换
    'url-encoder.html',             # 已存在
    'base64-encoder.html',          # 已存在
    'ascii-converter.html',         # 已存在
    'unicode-converter.html',       # Unicode转换
    'utf8-converter.html',          # UTF-8转换
    'utf16-converter.html',         # UTF-16转换
    
    # 数字和数学
    'number-base-converter.html',   # 进制转换
    'math-calculator.html',         # 数学计算器
    'unit-converter.html',          # 单位转换
    'percentage-calculator.html',   # 百分比计算器
    
    # 格式化和美化
    'json-formatter.html',          # 已存在
    'xml-formatter.html',           # XML格式化
    'yaml-formatter.html',          # YAML格式化
    'markdown-formatter.html',      # Markdown格式化
    'sql-formatter.html',           # SQL格式化
    'csv-formatter.html',           # CSV格式化
    
    # 数据处理
    'data-validator.html',          # 数据验证
    'data-cleaner.html',            # 数据清理
    'data-mapper.html',             # 数据映射
    'data-merger.html',             # 数据合并
    'data-extractor.html',          # 数据提取
    
    # 开发工具
    'regex-tester.html',            # 已存在
    'string-generator.html',        # 字符串生成器
    'password-generator.html',      # 密码生成器
    'random-number-generator.html', # 随机数生成器
    'uuid-generator.html',          # UUID生成器
    'guid-generator.html',          # GUID生成器
    'timestamp-converter.html',     # 已存在
]

# 获取我们当前的工具目录
def get_our_tools():
    tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'
    return set(os.listdir(tools_dir))

# 获取text.html中列出的工具
def get_tools_in_html():
    html_path = '/Users/macbookpro/Desktop/trae/oopenai2026/text.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取所有工具链接
    import re
    tool_links = re.findall(r'<a href="tools/(.*?)" class="tool-card-link">', html_content)
    return set(tool_links)

# 检查缺少的工具
def check_missing_jsoncn_tools():
    our_tools = get_our_tools()
    tools_in_html = get_tools_in_html()
    
    # 找出json.cn可能提供但我们还没有的工具
    missing_tools = [tool for tool in jsoncn_possible_tools if tool not in our_tools]
    
    # 找出我们已经实现但未在text.html中列出的工具
    unlisted_our_tools = [tool for tool in our_tools if 
                         (tool.startswith('text-') or tool.startswith('word-') or 
                          tool.startswith('line-') or tool.startswith('case-') or 
                          tool in jsoncn_possible_tools) and tool not in tools_in_html]
    
    print("=== json.cn可能提供但我们缺少的工具 ===")
    for tool in missing_tools:
        print(f"- {tool}")
    print(f"\n缺少的工具总数: {len(missing_tools)}")
    
    print("\n=== 我们已实现但未在text.html中列出的工具 ===")
    for tool in unlisted_our_tools:
        print(f"- {tool}")
    print(f"\n未列出的工具总数: {len(unlisted_our_tools)}")

if __name__ == "__main__":
    check_missing_jsoncn_tools()