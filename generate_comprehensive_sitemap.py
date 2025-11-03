#!/usr/bin/env python3
# Script to generate a comprehensive sitemap.xml for OOPEN AII website

import os
import datetime

def generate_sitemap():
    # Get current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Start sitemap XML
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://openai2026.com/</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://openai2026.com/encry.html</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://openai2026.com/code.html</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://openai2026.com/network.html</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://openai2026.com/dav.html</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://openai2026.com/contact.html</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://openai2026.com/privacy.html</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://openai2026.com/terms.html</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    
    # Add all tool pages
    tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'
    if os.path.exists(tools_dir):
        for filename in sorted(os.listdir(tools_dir)):
            if filename.endswith('.html'):
                # Determine priority based on file type
                priority = "0.8"
                # Image tools might get higher priority
                if filename.startswith('image-'):
                    priority = "0.85"
                    
                sitemap += f'''
  <url>
    <loc>https://openai2026.com/tools/{filename}</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>'''
    
    # Close the XML
    sitemap += "\n</urlset>"
    
    # Write to file
    with open('/Users/macbookpro/Desktop/trae/oopenai2026/sitemap.xml', 'w') as f:
        f.write(sitemap)
    
    print(f"Sitemap generated successfully with {sitemap.count('<url>')} URLs")
    print("File saved to: /Users/macbookpro/Desktop/trae/oopenai2026/sitemap.xml")

if __name__ == "__main__":
    generate_sitemap()