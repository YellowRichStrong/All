#!/usr/bin/env python3
# 自动更新站点地图脚本 - 监控文件变化并定期更新sitemap.xml

import os
import time
import datetime
import sys
from pathlib import Path

# 尝试导入schedule库，如果不存在则只支持手动模式
try:
    import schedule
    schedule_available = True
except ImportError:
    schedule_available = False
    print("警告: 未安装schedule库，仅支持手动更新模式")

# 配置
BASE_DIR = '/Users/macbookpro/Desktop/trae/oopenai2026'
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
SITEMAP_FILE = os.path.join(BASE_DIR, 'sitemap.xml')
GENERATOR_SCRIPT = os.path.join(BASE_DIR, 'generate_comprehensive_sitemap.py')
CHECK_INTERVAL = 3600  # 默认检查间隔（秒）- 1小时

# 存储上次修改时间
last_modified_times = {}

# 打印带有时间戳的日志
def log(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# 运行现有脚本生成站点地图
def generate_sitemap():
    try:
        log("开始更新站点地图...")
        # 导入并运行现有脚本中的函数
        sys.path.append(os.path.dirname(GENERATOR_SCRIPT))
        import generate_comprehensive_sitemap
        generate_comprehensive_sitemap.generate_sitemap()
        log("站点地图更新成功！")
        return True
    except Exception as e:
        log(f"生成站点地图时出错: {str(e)}")
        return False

# 检查文件是否已更改
def check_files_changed():
    log("检查文件变化...")
    changed = False
    
    # 检查根目录下的HTML文件
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
    for filename in html_files:
        file_path = os.path.join(BASE_DIR, filename)
        current_mtime = os.path.getmtime(file_path)
        
        if filename not in last_modified_times or last_modified_times[filename] != current_mtime:
            last_modified_times[filename] = current_mtime
            log(f"检测到变化: {filename}")
            changed = True
    
    # 检查tools目录下的HTML文件
    if os.path.exists(TOOLS_DIR):
        for filename in os.listdir(TOOLS_DIR):
            if filename.endswith('.html'):
                file_path = os.path.join(TOOLS_DIR, filename)
                current_mtime = os.path.getmtime(file_path)
                
                if filename not in last_modified_times or last_modified_times[filename] != current_mtime:
                    last_modified_times[filename] = current_mtime
                    log(f"检测到变化: tools/{filename}")
                    changed = True
    
    return changed

# 初始化文件修改时间记录
def init_modified_times():
    log("初始化文件修改时间记录...")
    
    # 记录根目录下的HTML文件
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
    for filename in html_files:
        file_path = os.path.join(BASE_DIR, filename)
        last_modified_times[filename] = os.path.getmtime(file_path)
    
    # 记录tools目录下的HTML文件
    if os.path.exists(TOOLS_DIR):
        for filename in os.listdir(TOOLS_DIR):
            if filename.endswith('.html'):
                file_path = os.path.join(TOOLS_DIR, filename)
                last_modified_times[filename] = os.path.getmtime(file_path)
    
    log(f"已记录 {len(last_modified_times)} 个文件的修改时间")

# 定时任务函数
def scheduled_task():
    if check_files_changed():
        generate_sitemap()

# 启动监控服务
def start_monitoring(interval=CHECK_INTERVAL, run_manually=False):
    # 初始化文件修改时间
    init_modified_times()
    
    # 首次运行生成站点地图
    generate_sitemap()
    
    if run_manually:
        # 只运行一次并退出
        log("手动模式: 站点地图已更新，程序退出")
        return
    
    # 检查schedule库是否可用
    if not schedule_available:
        log("错误: 自动监控模式需要schedule库，请先安装: pip3 install schedule")
        return
    
    # 设置定时任务
    schedule.every(interval).seconds.do(scheduled_task)
    log(f"监控服务已启动，每 {interval} 秒检查一次文件变化")
    log("提示: 按 Ctrl+C 可以随时停止服务")
    
    try:
        # 持续运行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次是否有待执行的任务
    except KeyboardInterrupt:
        log("监控服务已停止")
    except Exception as e:
        log(f"监控服务遇到错误: {str(e)}")

# 主函数
def main():
    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description='站点地图自动更新工具')
    parser.add_argument('--interval', type=int, help='检查间隔（秒）')
    parser.add_argument('--manual', action='store_true', help='手动运行一次并退出')
    
    args = parser.parse_args()
    
    interval = args.interval if args.interval else CHECK_INTERVAL
    run_manually = args.manual
    
    log(f"启动站点地图更新工具 (自动监控模式: {not run_manually})")
    start_monitoring(interval, run_manually)

if __name__ == "__main__":
    main()