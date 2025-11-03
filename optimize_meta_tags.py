#!/usr/bin/env python3
# Script to optimize meta tags for better SEO

import os
import re

def get_category_from_filename(filename):
    """Determine tool category based on filename"""
    if 'image-' in filename:
        return 'Image Tools'
    elif any(enc in filename for enc in ['aes-', 'md5-', 'sha-', 'hmac-', 'encryption', 'jwt-', 'des-', 'base64-', 'ascii-', 'crc32-', 'ripemd160-', 'rabbit-', 'rc4-', 'shake-', 'keccak-', 'tripledes-']):
        return 'Encryption Tools'
    elif any(code in filename for code in ['css-', 'html-', 'js-', 'json-', 'sql-', 'xml-', 'minify', 'format', 'debugger', 'eval']):
        return 'Code Tools'
    elif any(net in filename for net in ['ip-', 'dns-', 'ping-', 'port-', 'traceroute', 'whois-', 'website-', 'http-', 'ssl-', 'network-']):
        return 'Network Tools'
    else:
        return 'Tools'

def get_tool_name_from_filename(filename):
    """Convert filename to human-readable tool name"""
    # Remove .html extension and replace hyphens with spaces
    name = filename.replace('.html', '').replace('-', ' ')
    # Capitalize each word
    return ' '.join(word.capitalize() for word in name.split())

def generate_optimized_title(tool_name, category):
    """Generate optimized title tag"""
    # Format: Tool Name - Category | OOPEN AII
    return f"{tool_name} - {category} | OOPEN AII"

def generate_meta_description(tool_name, category):
    """Generate optimized meta description"""
    base_descriptions = {
        'Image Tools': f'Free online {tool_name.lower()} to edit, convert, and optimize your images. Works in your browser with no installation required.',
        'Encryption Tools': f'Free online {tool_name.lower()} for secure encryption and decryption. Protect your data with our powerful yet easy-to-use tool.',
        'Code Tools': f'Professional {tool_name.lower()} for developers. Format, minify, and optimize your code quickly and efficiently.',
        'Network Tools': f'Comprehensive {tool_name.lower()} for network diagnostics. Check connectivity, IP information, and domain details.'
    }
    
    base_desc = base_descriptions.get(category, f'Free online {tool_name.lower()} to help you complete your tasks quickly and efficiently.')
    return base_desc + ' 100% free with no registration needed. Try it now!'

def generate_meta_keywords(tool_name, category):
    """Generate optimized meta keywords"""
    # Base keywords based on category
    base_keywords = {
        'Image Tools': ['online image tools', 'free image editor', 'image converter', 'image optimizer', 'image processing'],
        'Encryption Tools': ['encryption tool', 'decryption', 'online encryption', 'security tools', 'data protection'],
        'Code Tools': ['code formatter', 'code minifier', 'development tools', 'online code editor', 'programming utilities'],
        'Network Tools': ['network tools', 'ip lookup', 'dns check', 'online network utilities', 'internet diagnostics']
    }
    
    keywords = base_keywords.get(category, [])
    # Add tool-specific keywords
    tool_keywords = tool_name.lower().split()
    keywords.extend(tool_keywords)
    # Add general keywords
    keywords.extend(['free online tool', 'no registration', 'browser-based', 'oopen ai'])
    
    # Remove duplicates and join
    return ', '.join(list(set(keywords)))

def optimize_meta_tags(file_path):
    """Optimize meta tags in a given HTML file"""
    filename = os.path.basename(file_path)
    
    # Skip non-HTML files
    if not filename.endswith('.html'):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip main category pages for now (they have custom content)
    if filename in ['index.html', 'encry.html', 'code.html', 'network.html', 'dav.html']:
        return False
    
    # Get tool information
    tool_name = get_tool_name_from_filename(filename)
    category = get_category_from_filename(filename)
    
    # Generate optimized tags
    title = generate_optimized_title(tool_name, category)
    description = generate_meta_description(tool_name, category)
    keywords = generate_meta_keywords(tool_name, category)
    
    # Update title tag
    updated_content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content, flags=re.DOTALL)
    
    # Update meta description
    if '<meta name="description"' in updated_content:
        updated_content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">', updated_content, flags=re.DOTALL)
    else:
        # Insert after title if not found
        updated_content = re.sub(r'</title>', f'</title>\n    <meta name="description" content="{description}">', updated_content)
    
    # Update meta keywords
    if '<meta name="keywords"' in updated_content:
        updated_content = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{keywords}">', updated_content, flags=re.DOTALL)
    else:
        # Insert after description if not found
        updated_content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">\n    <meta name="keywords" content="{keywords}">', updated_content, flags=re.DOTALL)
    
    # Write updated content back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Optimized meta tags for {filename}")
    return True

def optimize_all_meta_tags():
    """Optimize meta tags for all HTML files"""
    tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'
    count = 0
    
    if os.path.exists(tools_dir):
        for filename in os.listdir(tools_dir):
            file_path = os.path.join(tools_dir, filename)
            if optimize_meta_tags(file_path):
                count += 1
    
    print(f"Total pages with optimized meta tags: {count}")

if __name__ == "__main__":
    optimize_all_meta_tags()