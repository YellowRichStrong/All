#!/bin/bash

# 函数：在footer-links中添加blog链接
add_blog_link() {
    local file=$1
    
    # 检查文件是否是HTML文件
    if [[ "$file" == *.html ]]; then
        echo "处理文件: $file"
        
        # 检查文件是否已经包含blog/index.html链接
        if grep -q '"blog/index.html"' "$file"; then
            echo "  已存在blog链接，跳过: $file"
            return
        fi
        
        # 根据文件所在目录确定相对路径
        if [[ "$file" == */tools/* ]]; then
            BLOG_PATH="../blog/index.html"
        else
            BLOG_PATH="blog/index.html"
        fi
        
        # 在footer-links中的Home链接后面添加Blog链接
        sed -i '' 's/<a href="\(\.\.\/\)\?index.html">Home<\/a>/<a href="\1index.html">Home<\/a>\n                        <a href="'"$BLOG_PATH"'">Blog<\/a>/g' "$file"
        
        echo "  已添加blog链接: $file"
    fi
}

# 遍历当前目录下的所有HTML文件
find /Users/macbookpro/Desktop/trae/oopenai2026 -name "*.html" -type f | while read file; do
    add_blog_link "$file"
done

echo "所有文件处理完成！"