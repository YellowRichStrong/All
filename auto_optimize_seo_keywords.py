#!/usr/bin/env python3
# 自动SEO关键词优化脚本 - 每15天定期更新优化全网站的SEO关键词

import os
import time
import datetime
import sys
import schedule
import subprocess
from pathlib import Path

# 配置
BASE_DIR = '/Users/macbookpro/Desktop/trae/oopenai2026'
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
SEO_LOG_FILE = os.path.join(BASE_DIR, 'seo_optimization_log.txt')
META_TAGS_SCRIPT = os.path.join(BASE_DIR, 'optimize_meta_tags.py')
STRUCTURED_DATA_SCRIPT = os.path.join(BASE_DIR, 'add_structured_data.py')
UPDATE_INTERVAL_DAYS = 7  # 更新间隔（天）- 已从15天减少到7天以提高SEO效果

# 打印带有时间戳的日志
def log(message, write_to_file=True):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    if write_to_file:
        try:
            with open(SEO_LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"无法写入日志文件: {str(e)}")

# 执行meta标签优化
def run_meta_tags_optimization():
    try:
        log("开始优化meta标签和关键词...")
        
        # 检查脚本是否存在
        if not os.path.exists(META_TAGS_SCRIPT):
            log("错误: 未找到optimize_meta_tags.py脚本，执行自定义优化逻辑")
            # 如果脚本不存在，执行内置的优化逻辑
            return custom_optimize_meta_tags()
        
        # 运行现有脚本
        result = subprocess.run(
            [sys.executable, META_TAGS_SCRIPT],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        if result.returncode == 0:
            # 解析输出结果
            output = result.stdout
            log(f"Meta标签优化成功完成")
            log(f"输出: {output.strip()}")
            return True
        else:
            log(f"Meta标签优化脚本执行失败: {result.stderr}")
            # 如果脚本执行失败，尝试内置优化逻辑
            return custom_optimize_meta_tags()
    except Exception as e:
        log(f"执行meta标签优化时出错: {str(e)}")
        # 尝试内置优化逻辑作为备用
        return custom_optimize_meta_tags()

# 自定义meta标签优化逻辑（备用）
def custom_optimize_meta_tags():
    try:
        log("使用备用优化逻辑进行meta标签优化...")
        
        count = 0
        # 优化主页面
        main_pages = ['index.html', 'encry.html', 'code.html', 'network.html', 'dav.html', 'text.html']
        for page in main_pages:
            page_path = os.path.join(BASE_DIR, page)
            if os.path.exists(page_path):
                if optimize_single_page(page_path, is_main_page=True):
                    count += 1
        
        # 优化工具页面
        if os.path.exists(TOOLS_DIR):
            for filename in os.listdir(TOOLS_DIR):
                if filename.endswith('.html'):
                    file_path = os.path.join(TOOLS_DIR, filename)
                    if optimize_single_page(file_path):
                        count += 1
        
        log(f"自定义优化完成，共优化 {count} 个页面")
        return True
    except Exception as e:
        log(f"自定义优化失败: {str(e)}")
        return False

# 优化单个页面的meta标签
def optimize_single_page(file_path, is_main_page=False):
    try:
        import re
        filename = os.path.basename(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取页面信息
        if is_main_page:
            page_name = get_main_page_name(filename)
            category = get_main_page_category(filename)
        else:
            page_name = get_tool_name_from_filename(filename)
            category = get_category_from_filename(filename)
        
        # 生成优化的标签
        title = generate_optimized_title(page_name, category, is_main_page)
        description = generate_meta_description(page_name, category, is_main_page)
        keywords = generate_meta_keywords(page_name, category, is_main_page)
        
        # 更新title标签
        updated_content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content, flags=re.DOTALL)
        
        # 更新meta description
        if '<meta name="description"' in updated_content:
            updated_content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">', updated_content, flags=re.DOTALL)
        else:
            # 插入到title之后
            updated_content = re.sub(r'</title>', f'</title>\n    <meta name="description" content="{description}">', updated_content)
        
        # 更新meta keywords
        if '<meta name="keywords"' in updated_content:
            updated_content = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{keywords}">', updated_content, flags=re.DOTALL)
        else:
            # 插入到description之后
            updated_content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">\n    <meta name="keywords" content="{keywords}">', updated_content, flags=re.DOTALL)
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        log(f"优化页面: {filename}")
        return True
    except Exception as e:
        log(f"优化页面 {os.path.basename(file_path)} 失败: {str(e)}")
        return False

# 获取主页面名称
def get_main_page_name(filename):
    page_names = {
        'index.html': 'OOPEN AII',
        'encry.html': 'Encryption Tools',
        'code.html': 'Code Tools',
        'network.html': 'Network Tools',
        'dav.html': 'DAV Tools',
        'text.html': 'Text Tools'
    }
    return page_names.get(filename, 'OOPEN AII')

# 获取主页面类别
def get_main_page_category(filename):
    if filename == 'index.html':
        return 'Free Online Tools'
    return get_main_page_name(filename)

# 获取工具名称（从文件名）
def get_tool_name_from_filename(filename):
    name = filename.replace('.html', '').replace('-', ' ')
    return ' '.join(word.capitalize() for word in name.split())

# 获取工具类别
def get_category_from_filename(filename):
    if 'image-' in filename:
        return 'Image Tools'
    elif any(enc in filename for enc in ['aes-', 'md5-', 'sha-', 'hmac-', 'encryption', 'jwt-', 'des-', 'base64-', 'ascii-', 'crc32-', 'ripemd160-', 'rabbit-', 'rc4-', 'shake-', 'keccak-', 'tripledes-']):
        return 'Encryption Tools'
    elif any(code in filename for code in ['css-', 'html-', 'js-', 'json-', 'sql-', 'xml-', 'minify', 'format', 'debugger', 'eval']):
        return 'Code Tools'
    elif any(net in filename for net in ['ip-', 'dns-', 'ping-', 'port-', 'traceroute', 'whois-', 'website-', 'http-', 'ssl-', 'network-']):
        return 'Network Tools'
    elif any(text in filename for text in ['text-', 'word-', 'line-', 'string-', 'lorem-', 'pinyin-']):
        return 'Text Tools'
    else:
        return 'DAV Tools'

# 生成优化的标题
def generate_optimized_title(page_name, category, is_main_page=False):
    if is_main_page:
        if page_name == 'OOPEN AII':
            return "OOPEN AII - Free Online Tools for Images, Code, Encryption & More"
        return f"{page_name} - Free Online Tools | OOPEN AII"
    return f"{page_name} - {category} | OOPEN AII"

# 生成meta描述
def generate_meta_description(page_name, category, is_main_page=False):
    if is_main_page:
        if page_name == 'OOPEN AII':
            return "Free online tools for image editing, encryption, coding, and network diagnostics. All tools work in your browser with no installation required. 100% free and secure."
        
        descriptions = {
            'Encryption Tools': "Comprehensive collection of free online encryption tools. Secure your data with AES, MD5, SHA, Base64 and more. Works in your browser, no installation needed.",
            'Code Tools': "Professional code tools for developers. Format, minify, and optimize CSS, HTML, JavaScript, JSON, XML and SQL code quickly and efficiently.",
            'Network Tools': "Essential network diagnostics tools for IT professionals. Check IP information, DNS, ping, ports, and website performance from your browser.",
            'Text Tools': "Powerful text processing tools for writers and developers. Count words, convert case, extract text, compare strings, and more - all for free.",
            'DAV Tools': "Specialized tools for data analysis and visualization. Convert formats, generate data, and process information with our easy-to-use online utilities."
        }
        return descriptions.get(category, f"Free online {page_name.lower()} for various tasks. Works in your browser with no installation required.")
    
    # 工具页面描述
    base_descriptions = {
        'Image Tools': f'Free online {page_name.lower()} to edit, convert, and optimize your images. Works in your browser with no installation required. 100% free and secure.',
        'Encryption Tools': f'Free online {page_name.lower()} for secure encryption and decryption. Protect your data with our powerful yet easy-to-use tool. No registration needed.',
        'Code Tools': f'Professional {page_name.lower()} for developers. Format, minify, and optimize your code quickly and efficiently. Try it now!',
        'Network Tools': f'Comprehensive {page_name.lower()} for network diagnostics. Check connectivity, IP information, and domain details. Works from any browser.',
        'Text Tools': f'Advanced {page_name.lower()} for text processing. Analyze, convert, and manipulate text data with our free online utility. No software to install.',
        'DAV Tools': f'Free online {page_name.lower()} for data processing. Convert, generate, and analyze data with ease. Works in your browser, completely free.'
    }
    
    return base_descriptions.get(category, f'Free online {page_name.lower()} to help you complete your tasks quickly and efficiently. 100% free with no registration needed.')

# 生成优化的meta关键词
def generate_meta_keywords(page_name, category, is_main_page=False):
    # 基础关键词库 - 已扩展，增加更多长尾关键词
    base_keywords = {
        'Image Tools': ['online image tools', 'free image editor', 'image converter', 'image optimizer', 
                        'image processing', 'photo editor online', 'image resize', 'compress images',
                        'image cropping tool', 'image watermark online', 'convert image format free', 
                        'resize image without losing quality', 'image optimization online', 
                        'batch image processing tools', 'webp converter online'],
        'Encryption Tools': ['encryption tool', 'decryption', 'online encryption', 'security tools', 
                            'data protection', 'aes encryption', 'md5 hash', 'base64 encoder',
                            'secure data encryption', 'online password generator', 'hash calculator online',
                            'encrypt text online free', 'decrypt base64 online', 'secure hash algorithm',
                            'encryption for web developers'],
        'Code Tools': ['code formatter', 'code minifier', 'development tools', 'online code editor', 
                      'programming utilities', 'css formatter', 'json formatter', 'javascript beautifier',
                      'code optimization tools', 'online code analyzer', 'minify code for web',
                      'format json online free', 'beautify javascript code', 'debug code online',
                      'programming productivity tools'],
        'Network Tools': ['network tools', 'ip lookup', 'dns check', 'online network utilities', 
                          'internet diagnostics', 'ping test', 'port scanner', 'whois lookup',
                          'check website status', 'dns lookup tool', 'network speed test online',
                          'ip address location finder', 'website performance checker', 'ssl certificate checker',
                          'network diagnostic utilities'],
        'Text Tools': ['text tools', 'word counter', 'text converter', 'string tools', 
                      'text analyzer', 'character count', 'lorem ipsum generator', 'text comparison',
                      'online text editor', 'word frequency analyzer', 'text to speech converter',
                      'convert text to different formats', 'text statistics calculator', 'online plagiarism checker',
                      'text manipulation tools'],
        'DAV Tools': ['data tools', 'data converter', 'data analysis', 'online utilities', 
                     'free tools', 'web tools', 'browser tools', 'productivity tools',
                     'data visualization tools', 'online data processing', 'convert data formats',
                     'data analysis for beginners', 'web data tools', 'productivity enhancement tools',
                     'online data utilities']
    }
    
    keywords = base_keywords.get(category, [])
    
    # 添加页面特定关键词
    if is_main_page:
        if page_name != 'OOPEN AII':
            keywords.extend(page_name.lower().split())
    else:
        # 工具页面添加更多特定关键词
        tool_keywords = page_name.lower().split()
        keywords.extend(tool_keywords)
        # 从文件名提取更多关键词（保留连字符形式）
        filename = page_name.lower().replace(' ', '-')
        if '-' in filename:
            keywords.append(filename)
    
    # 添加通用关键词 - 增加更多与SEO相关的长尾关键词
    common_keywords = ['free online tool', 'no registration', 'browser-based', 'oopen ai', 'free tool', 
                      'online utility', 'web application', 'no installation', 'best free online tools',
                      'top web utilities', 'free browser tools', 'no download required', 
                      'instant results', 'user friendly tools', 'online tools without registration',
                      'free web applications', 'quick and easy tools', 'tools for web developers',
                      'best online utilities 2024']
    keywords.extend(common_keywords)
    
    # 添加SEO相关关键词 - 增加更多搜索引擎优化关键词
    if is_main_page:
        keywords.extend(['best online tools', 'free web tools', 'internet tools', 'online services',
                        'top online tools website', 'comprehensive web tools', 'best free tools online',
                        'online tools collection', 'best tools for web developers', 'free online utilities',
                        'all in one web tools', 'must have online tools', 'best internet utilities'])
    
    # 去重并限制数量
    unique_keywords = list(set(keywords))
    # 优先保留更相关的关键词
    prioritized_keywords = []
    # 首先添加与页面名称和类别相关的关键词
    page_name_lower = page_name.lower()
    category_lower = category.lower()
    
    for keyword in unique_keywords:
        if page_name_lower in keyword or any(word in keyword for word in page_name_lower.split()) or category_lower in keyword:
            prioritized_keywords.append(keyword)
    
    # 添加剩余关键词
    for keyword in unique_keywords:
        if keyword not in prioritized_keywords:
            prioritized_keywords.append(keyword)
    
    # 限制关键词数量，避免过长
    max_keywords = 20 if is_main_page else 15
    limited_keywords = prioritized_keywords[:max_keywords]
    
    return ', '.join(limited_keywords)

# 执行结构化数据标记
def run_structured_data_markup():
    try:
        log("开始添加结构化数据标记...")
        
        # 检查脚本是否存在
        if not os.path.exists(STRUCTURED_DATA_SCRIPT):
            log("错误: 未找到add_structured_data.py脚本")
            return False
        
        # 运行结构化数据脚本
        result = subprocess.run(
            [sys.executable, STRUCTURED_DATA_SCRIPT],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        if result.returncode == 0:
            log(f"结构化数据标记成功完成")
            log(f"输出: {result.stdout.strip()}")
            return True
        else:
            log(f"结构化数据标记脚本执行失败: {result.stderr}")
            return False
    except Exception as e:
        log(f"执行结构化数据标记时出错: {str(e)}")
        return False

# 更新站点地图
def update_sitemap():
    try:
        log("更新站点地图...")
        sitemap_script = os.path.join(BASE_DIR, 'generate_comprehensive_sitemap.py')
        
        if os.path.exists(sitemap_script):
            result = subprocess.run(
                [sys.executable, sitemap_script],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                log("站点地图更新成功")
                return True
            else:
                log(f"站点地图更新失败: {result.stderr}")
                return False
        else:
            log("未找到站点地图生成脚本")
            return False
    except Exception as e:
        log(f"更新站点地图时出错: {str(e)}")
        return False

# 执行完整的SEO优化
def perform_complete_seo_optimization():
    log("="*60)
    log("开始执行完整的SEO关键词优化")
    log("="*60)
    
    # 记录优化开始时间
    start_time = time.time()
    
    # 执行meta标签优化
    meta_tags_success = run_meta_tags_optimization()
    
    # 添加结构化数据标记（新功能）
    structured_data_success = run_structured_data_markup()
    
    # 更新站点地图
    sitemap_success = update_sitemap()
    
    # 记录优化结束时间
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    
    # 生成优化报告
    log("="*60)
    log(f"SEO优化完成，耗时: {execution_time} 秒")
    log(f"Meta标签优化: {'成功' if meta_tags_success else '失败'}")
    log(f"结构化数据标记: {'成功' if structured_data_success else '失败'}")
    log(f"站点地图更新: {'成功' if sitemap_success else '失败'}")
    log("="*60)
    
    return meta_tags_success and structured_data_success and sitemap_success

# 设置定时任务
def schedule_regular_optimization():
    # 每15天运行一次
    schedule.every(UPDATE_INTERVAL_DAYS).days.do(perform_complete_seo_optimization)
    log(f"已设置定期SEO优化任务，每 {UPDATE_INTERVAL_DAYS} 天执行一次")
    log("下次优化时间: " + (datetime.datetime.now() + datetime.timedelta(days=UPDATE_INTERVAL_DAYS)).strftime('%Y-%m-%d %H:%M:%S'))
    log("提示: 按 Ctrl+C 可以随时停止服务")

# 启动优化服务
def start_optimization_service(run_manually=False):
    log(f"启动SEO关键词自动优化服务 (自动模式: {not run_manually})")
    
    if run_manually:
        # 手动运行一次
        perform_complete_seo_optimization()
        log("手动优化完成，程序退出")
        return
    
    # 首次运行
    perform_complete_seo_optimization()
    
    # 设置定时任务
    schedule_regular_optimization()
    
    try:
        # 持续运行
        while True:
            schedule.run_pending()
            time.sleep(3600)  # 每小时检查一次是否有待执行的任务
    except KeyboardInterrupt:
        log("SEO优化服务已停止")
    except Exception as e:
        log(f"SEO优化服务遇到错误: {str(e)}")

# 主函数
def main():
    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description='SEO关键词自动优化工具')
    parser.add_argument('--manual', action='store_true', help='手动运行一次优化')
    parser.add_argument('--interval', type=int, help='自定义优化间隔（天）')
    
    args = parser.parse_args()
    
    # 如果指定了自定义间隔
    if args.interval and args.interval > 0:
        global UPDATE_INTERVAL_DAYS
        UPDATE_INTERVAL_DAYS = args.interval
        log(f"已设置自定义优化间隔: {UPDATE_INTERVAL_DAYS} 天")
    
    # 启动服务
    start_optimization_service(run_manually=args.manual)

if __name__ == "__main__":
    main()