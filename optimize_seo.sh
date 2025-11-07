#!/bin/bash

# SEO关键词自动优化启动脚本
# 提供便捷的SEO优化功能入口

echo "===================================="
echo "      SEO关键词自动优化工具       "
echo "===================================="
echo "每7天自动优化全网站SEO关键词"
echo "功能包括：meta标签优化、结构化数据标记、关键词更新、站点地图同步"
echo "===================================="

while true; do
    echo ""
    echo "请选择操作："
    echo "1. 手动运行一次SEO优化"
    echo "2. 启动自动优化服务（每7天）"
    echo "3. 自定义优化间隔"
    echo "4. 查看最近的优化日志"
    echo "5. 退出"
    
    read -p "请输入选择 (1-5): " choice
    
    case $choice in
        1)
            echo "开始手动运行SEO优化..."
            python3 auto_optimize_seo_keywords.py --manual
            echo "优化完成！"
            ;;
        2)
            echo "启动自动优化服务（每7天）..."
            echo "服务将在后台持续运行，每7天自动执行优化"
            python3 auto_optimize_seo_keywords.py
            ;;
        3)
            read -p "请输入优化间隔天数: " days
            if [[ $days =~ ^[0-9]+$ ]] && [ $days -gt 0 ]; then
                echo "启动自动优化服务（每$days天）..."
                python3 auto_optimize_seo_keywords.py --interval $days
            else
                echo "错误：请输入有效的天数！"
            fi
            ;;
        4)
            echo "最近的优化日志："
            echo "------------------------------------"
            tail -n 20 seo_optimization_log.txt
            ;;
        5)
            echo "退出程序"
            exit 0
            ;;
        *)
            echo "无效的选择，请重新输入"
            ;;
    esac
done