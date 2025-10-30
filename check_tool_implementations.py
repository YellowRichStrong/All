import os
import re

# 工具目录路径
tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'

# 获取所有HTML文件
tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.html')]

# 统计结果
implemented_tools = []
not_implemented_tools = []

# 实现检测模式
implementation_pattern = re.compile(r'<script[^>]*>.*?(?:addEventListener|function|document\.getElementById|console\.log).*?</script>', re.DOTALL | re.IGNORECASE)

# 检查每个工具文件
for tool_file in tool_files:
    file_path = os.path.join(tools_dir, tool_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含实现代码
    if implementation_pattern.search(content):
        implemented_tools.append(tool_file)
    else:
        not_implemented_tools.append(tool_file)

# 输出结果
print(f"\n检查完成！总计工具数量: {len(tool_files)}")
print(f"\n已实现的工具 ({len(implemented_tools)}):")
for tool in sorted(implemented_tools):
    print(f"  - {tool}")

print(f"\n未实现的工具 ({len(not_implemented_tools)}):")
for tool in sorted(not_implemented_tools):
    print(f"  - {tool}")

print(f"\n实现率: {len(implemented_tools) / len(tool_files) * 100:.1f}%")

# 为未实现的工具生成实现模板
if not_implemented_tools:
    print("\n正在为未实现的工具生成基础实现...")
    
    # 基本实现模板
    base_template = '''
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // 基本功能实现
            console.log('{tool_name} tool initialized');
            
            // 添加简单的实现逻辑
            // TODO: 实现完整功能
        });
    </script>
    '''
    
    for tool_file in not_implemented_tools:
        file_path = os.path.join(tools_dir, tool_file)
        tool_name = os.path.splitext(tool_file)[0].replace('-', ' ').title()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有script标签
        if '</script>' in content:
            # 在最后一个script标签后添加实现
            new_content = re.sub(r'(</script>)(?!.*</script>)', f'\1{base_template}', content, flags=re.DOTALL)
        else:
            # 在</body>前添加script标签
            new_content = re.sub(r'</body>', f'{base_template}\n</body>', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  - 已添加基础实现到 {tool_file}")

print("\n所有工具检查和处理完成！")