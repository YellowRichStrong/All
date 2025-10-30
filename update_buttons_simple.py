import os

def update_index_buttons():
    try:
        index_path = os.path.join(os.getcwd(), 'index.html')
        
        # 读取文件内容
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 定义需要替换的内容
        old_text = '<div class="tool-actions">\n                                    <span class="tool-btn">Use Tool</span>\n                                </div>'
        new_text = '<button class="tool-btn">Use Tool</button>'
        
        # 执行替换
        updated_content = content.replace(old_text, new_text)
        
        # 写回文件
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("Successfully updated index.html buttons")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    update_index_buttons()