import os

def update_tool_buttons(file_path):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用简单的字符串替换
        old_str = '<div class="tool-actions">\n                                    <span class="tool-btn">Use Tool</span>\n                                </div>'
        new_str = '<button class="tool-btn">Use Tool</button>'
        
        updated_content = content.replace(old_str, new_str)
        
        # 也处理可能的不同格式
        old_str2 = '<div class="tool-actions">\n                                    <span class="tool-btn">Use Tool</span>\n                                </div>'
        new_str2 = '<button class="tool-btn">Use Tool</button>'
        updated_content = updated_content.replace(old_str2, new_str2)
        
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
    # 首先更新index.html
    index_path = os.path.join(os.getcwd(), 'index.html')
    if update_tool_buttons(index_path):
        print("Updated index.html")
    
    print("Script completed.")

if __name__ == "__main__":
    main()