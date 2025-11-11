#!/usr/bin/env python3
import os
import subprocess
import time

# 检查关键页面是否可访问
def check_page_health(base_url, paths):
    print("开始检查网站健康状态...")
    print(f"基础URL: {base_url}")
    print("=" * 50)
    
    success = True
    for path in paths:
        url = f"{base_url}{path}"
        try:
            # 使用curl检查页面状态
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            status_code = result.stdout.strip()
            
            if status_code.startswith('2') or status_code.startswith('3'):
                print(f"✅ {path} - 状态码: {status_code}")
            else:
                print(f"❌ {path} - 状态码: {status_code}")
                success = False
        except Exception as e:
            print(f"❌ {path} - 错误: {str(e)}")
            success = False
    
    print("=" * 50)
    if success:
        print("✅ 网站健康检查通过！所有关键页面均可正常访问。")
    else:
        print("❌ 网站健康检查失败！部分页面无法正常访问。")
    
    return success

# 检查文件结构
def check_file_structure():
    print("\n检查网站文件结构...")
    print("=" * 50)
    
    required_files = [
        "index.html",
        "css/style.css",
        "js/main.js",
        "sitemap.xml"
    ]
    
    success = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ 文件存在: {file}")
        else:
            print(f"❌ 文件缺失: {file}")
            success = False
    
    # 检查工具页面数量
    tools_dir = "tools"
    if os.path.exists(tools_dir) and os.path.isdir(tools_dir):
        tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.html')]
        print(f"✅ 发现 {len(tool_files)} 个工具页面")
    else:
        print(f"❌ 工具目录不存在或无法访问: {tools_dir}")
        success = False
    
    # 检查博客页面数量
    blog_dir = "blog"
    if os.path.exists(blog_dir) and os.path.isdir(blog_dir):
        blog_files = [f for f in os.listdir(blog_dir) if f.endswith('.html')]
        print(f"✅ 发现 {len(blog_files)} 个博客页面")
    else:
        print(f"❌ 博客目录不存在或无法访问: {blog_dir}")
        success = False
    
    print("=" * 50)
    return success

# 主函数
def main():
    print("网站健康状态验证工具")
    print("=" * 50)
    
    # 关键页面路径
    critical_pages = [
        "/",
        "/index.html",
        "/about.html",
        "/contact.html",
        "/blog/index.html",
        "/tools/json-formatter.html",
        "/text.html",
        "/image.html",
        "/sitemap.xml"
    ]
    
    # 本地测试URL
    base_url = "http://localhost:8000"
    
    # 先检查文件结构
    file_structure_ok = check_file_structure()
    
    # 再检查页面访问状态
    page_health_ok = check_page_health(base_url, critical_pages)
    
    # 总结
    print("\n总结:")
    print("=" * 50)
    if file_structure_ok and page_health_ok:
        print("🎉 网站运行正常！所有检查均已通过。")
        return 0
    else:
        print("⚠️  网站存在问题，请查看上述详细信息。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)