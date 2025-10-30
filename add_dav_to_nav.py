import os
import re

def update_navbar(file_path):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换导航栏部分
        old_nav = '<nav>\s*<ul>\s*<li><a href="../index.html">Image Tools</a></li>\s*<li><a href="../about.html">About</a></li>\s*</ul>\s*</nav>'
        new_nav = '<nav>\n                <ul>\n                    <li><a href="../index.html">Image Tools</a></li>\n                    <li><a href="../dav.html">Dav</a></li>\n                    <li><a href="../about.html">About</a></li>\n                </ul>\n            </nav>'
        
        updated_content = re.sub(old_nav, new_nav, content, flags=re.DOTALL)
        
        # 如果内容有变化，写回文件
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    tools_dir = os.path.join(os.getcwd(), 'tools')
    image_tools = []
    
    # 识别图片工具（文件名包含image或img）
    for file in os.listdir(tools_dir):
        if file.endswith('.html') and ('image' in file.lower() or 'img' in file.lower()):
            image_tools.append(os.path.join(tools_dir, file))
    
    print(f"Found {len(image_tools)} image tool pages to update.")
    updated_count = 0
    
    for file_path in image_tools:
        if update_navbar(file_path):
            updated_count += 1
    
    print(f"Successfully updated {updated_count} files.")

if __name__ == "__main__":
    main()