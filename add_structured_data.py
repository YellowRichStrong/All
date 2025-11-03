#!/usr/bin/env python3
# Script to add Schema.org structured data to HTML pages

import os
import re

# Get tool name from filename
def get_tool_name(filename):
    # Remove .html extension and replace hyphens with spaces
    name = filename.replace('.html', '').replace('-', ' ')
    # Capitalize each word
    return ' '.join(word.capitalize() for word in name.split())

# Get tool description based on filename
def get_tool_description(filename):
    tool_name = get_tool_name(filename)
    
    # Base descriptions
    descriptions = {
        'image': f'A powerful {tool_name} tool that lets you edit and manipulate your images directly in your browser. No installation required and completely free to use.',
        'encryption': f'A secure {tool_name} tool that provides encryption and decryption services right in your browser. Your data never leaves your computer, ensuring complete privacy.',
        'code': f'A professional {tool_name} tool designed for developers to format, minify, and optimize code quickly and efficiently.',
        'network': f'A comprehensive {tool_name} tool that helps you diagnose network issues, check connectivity, and gather information about IP addresses and domains.'
    }
    
    # Determine category based on filename
    if 'image-' in filename:
        return descriptions['image']
    elif any(enc in filename for enc in ['aes-', 'md5-', 'sha-', 'hmac-', 'encryption', 'jwt-', 'des-', 'base64-', 'ascii-']):
        return descriptions['encryption']
    elif any(code in filename for code in ['css-', 'html-', 'js-', 'json-', 'sql-', 'xml-', 'minify', 'format']):
        return descriptions['code']
    elif any(net in filename for net in ['ip-', 'dns-', 'ping-', 'port-', 'traceroute', 'whois-', 'website-']):
        return descriptions['network']
    else:
        return f'A useful {tool_name} tool that helps you complete your tasks quickly and efficiently. Free to use with no registration required.'

# Add structured data to a file
def add_structured_data_to_file(file_path):
    filename = os.path.basename(file_path)
    
    # Skip non-HTML files and special files
    if not filename.endswith('.html') or filename in ['index.html', 'encry.html', 'code.html', 'network.html', 'dav.html']:
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if structured data already exists
    if 'application/ld+json' in content:
        print(f"Structured data already exists in {filename}")
        return False
    
    tool_name = get_tool_name(filename)
    tool_description = get_tool_description(filename)
    tool_url = f"https://openai2026.com/tools/{filename}"
    
    # Create structured data JSON
    structured_data = f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "{tool_name}",
      "applicationCategory": "WebApplication",
      "operatingSystem": "Web",
      "offers": {{
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }},
      "description": "{tool_description}",
      "url": "{tool_url}",
      "provider": {{
        "@type": "Organization",
        "name": "OOPEN AII",
        "url": "https://openai2026.com/"
      }}
    }}
    </script>
    '''
    
    # Insert structured data before </head> tag
    updated_content = re.sub(r'</head>', structured_data + '\n</head>', content)
    
    # Write updated content back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Added structured data to {filename}")
    return True

# Add structured data to all tool pages
def add_structured_data_to_all_pages():
    tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'
    count = 0
    
    if os.path.exists(tools_dir):
        for filename in os.listdir(tools_dir):
            file_path = os.path.join(tools_dir, filename)
            if add_structured_data_to_file(file_path):
                count += 1
    
    # Add structured data to main pages
    main_pages = ['/Users/macbookpro/Desktop/trae/oopenai2026/index.html']
    for page in main_pages:
        if os.path.exists(page):
            # For homepage, use WebSite schema
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if structured data already exists
            if 'application/ld+json' not in content:
                website_structured_data = '''
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "OOPEN AII - Free Online Tools",
      "url": "https://openai2026.com/",
      "description": "Free online tools for image editing, encryption, coding, and network diagnostics. All tools work in your browser with no installation required.",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://openai2026.com/search?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
    </script>
    '''
                
                updated_content = re.sub(r'</head>', website_structured_data + '\n</head>', content)
                
                with open(page, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"Added structured data to index.html")
                count += 1
    
    print(f"Total pages updated: {count}")

if __name__ == "__main__":
    add_structured_data_to_all_pages()