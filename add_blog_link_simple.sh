#!/bin/bash

# 遍历所有HTML文件
find /Users/macbookpro/Desktop/trae/oopenai2026 -name "*.html" -type f | while read file; do
    echo "处理: $file"
    
    # 检查是否已经包含blog链接
    if grep -q 'blog/index.html' "$file"; then
        echo "  已存在，跳过"
        continue
    fi
    
    # 根据文件路径确定相对路径
    if [[ "$file" == */tools/* ]]; then
        BLOG_LINK="<a href=\"../blog/index.html\">Blog</a>"
    else
        BLOG_LINK="<a href=\"blog/index.html\">Blog</a>"
    fi
    
    # 使用更简单的sed命令，在Home链接后面添加Blog链接
    sed -i '' '/<a href=\"\(\.\.\/\)\?index.html\">Home<\/a>/a\\        '$BLOG_LINK'' "$file"
    
    echo "  已添加blog链接"
done

echo "所有文件处理完成！"