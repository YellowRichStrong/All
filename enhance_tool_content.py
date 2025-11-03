#!/usr/bin/env python3
# Script to enhance tool page content for better SEO and user experience

import os
import re

def get_tool_category(filename):
    """Determine tool category based on filename"""
    if 'image-' in filename:
        return 'Image'
    elif any(enc in filename for enc in ['aes-', 'md5-', 'sha-', 'hmac-', 'encryption', 'jwt-', 'des-', 'base64-', 'ascii-']):
        return 'Encryption'
    elif any(code in filename for code in ['css-', 'html-', 'js-', 'json-', 'sql-', 'xml-', 'minify', 'format']):
        return 'Code'
    elif any(net in filename for net in ['ip-', 'dns-', 'ping-', 'port-', 'traceroute', 'whois-', 'website-']):
        return 'Network'
    else:
        return 'General'

def get_tool_name(filename):
    """Convert filename to human-readable tool name"""
    # Remove .html extension and replace hyphens with spaces
    name = filename.replace('.html', '').replace('-', ' ')
    # Capitalize each word
    return ' '.join(word.capitalize() for word in name.split())

def generate_usage_guide(category):
    """Generate usage guide based on tool category"""
    guides = {
        'Image': '''
<div class="how-to-use">
    <h3>How to Use This Tool</h3>
    <ol>
        <li><strong>Upload Your Image</strong>: Click the upload button or drag and drop your image file.</li>
        <li><strong>Configure Settings</strong>: Adjust the tool settings according to your needs.</li>
        <li><strong>Process Your Image</strong>: Click the process button to apply changes.</li>
        <li><strong>Preview and Download</strong>: Preview the result and download your processed image.</li>
    </ol>
</div>''',
        'Encryption': '''
<div class="how-to-use">
    <h3>How to Use This Tool</h3>
    <ol>
        <li><strong>Enter Your Data</strong>: Input the text or upload the file you want to process.</li>
        <li><strong>Configure Options</strong>: Set any necessary parameters or keys for the encryption/decryption.</li>
        <li><strong>Process Your Data</strong>: Click the process button to encrypt or decrypt your data.</li>
        <li><strong>Copy the Result</strong>: Copy the processed result to your clipboard.</li>
    </ol>
</div>''',
        'Code': '''
<div class="how-to-use">
    <h3>How to Use This Tool</h3>
    <ol>
        <li><strong>Paste Your Code</strong>: Copy and paste your code into the input area.</li>
        <li><strong>Select Options</strong>: Choose the desired formatting, minification, or conversion options.</li>
        <li><strong>Process Your Code</strong>: Click the process button to apply the changes.</li>
        <li><strong>Copy the Result</strong>: Copy the processed code back to your project.</li>
    </ol>
</div>''',
        'Network': '''
<div class="how-to-use">
    <h3>How to Use This Tool</h3>
    <ol>
        <li><strong>Enter Your Input</strong>: Type in the IP address, domain, or other required information.</li>
        <li><strong>Start the Scan</strong>: Click the lookup or scan button to begin the process.</li>
        <li><strong>View Results</strong>: Review the detailed information provided by the tool.</li>
        <li><strong>Copy or Export</strong>: Copy the results or export them as needed.</li>
    </ol>
</div>''',
        'General': '''
<div class="how-to-use">
    <h3>How to Use This Tool</h3>
    <ol>
        <li><strong>Enter Your Input</strong>: Type in or upload the data you want to process.</li>
        <li><strong>Configure Settings</strong>: Adjust any available options for the tool.</li>
        <li><strong>Process Your Data</strong>: Click the process button to run the tool.</li>
        <li><strong>Copy Results</strong>: Copy the output to use in your project.</li>
    </ol>
</div>'''
    }
    return guides.get(category, guides['General'])

def generate_benefits_section(category, tool_name):
    """Generate benefits section based on tool category"""
    benefits = {
        'Image': f'''
<div class="tool-benefits">
    <h3>Why Use Our {tool_name}</h3>
    <ul>
        <li>100% free and no registration required</li>
        <li>Works entirely in your browser - no downloads needed</li>
        <li>High-quality image processing algorithms</li>
        <li>Preserves image quality while optimizing size</li>
        <li>Batch processing capabilities (for supported tools)</li>
        <li>Mobile-friendly interface</li>
    </ul>
</div>''',
        'Encryption': f'''
<div class="tool-benefits">
    <h3>Why Use Our {tool_name}</h3>
    <ul>
        <li>Secure processing - your data never leaves your browser</li>
        <li>Multiple encryption algorithms supported</li>
        <li>Professional-grade security features</li>
        <li>Intuitive interface for complex operations</li>
        <li>Detailed documentation and examples</li>
        <li>Free for personal and commercial use</li>
    </ul>
</div>''',
        'Code': f'''
<div class="tool-benefits">
    <h3>Why Use Our {tool_name}</h3>
    <ul>
        <li>Optimized for developers' workflows</li>
        <li>Supports multiple programming languages</li>
        <li>Customizable formatting options</li>
        <li>Fast processing even for large code files</li>
        <li>Error detection and highlighting</li>
        <li>Regularly updated with new features</li>
    </ul>
</div>''',
        'Network': f'''
<div class="tool-benefits">
    <h3>Why Use Our {tool_name}</h3>
    <ul>
        <li>Accurate and reliable network information</li>
        <li>Fast processing and response times</li>
        <li>Comprehensive diagnostic capabilities</li>
        <li>Detailed technical information for network professionals</li>
        <li>Easy-to-understand results for beginners</li>
        <li>Free unlimited use</li>
    </ul>
</div>''',
        'General': f'''
<div class="tool-benefits">
    <h3>Why Use Our {tool_name}</h3>
    <ul>
        <li>Simple and intuitive interface</li>
        <li>Fast and efficient processing</li>
        <li>No software installation required</li>
        <li>Free to use with no limitations</li>
        <li>Works on all modern browsers</li>
        <li>Regularly maintained and updated</li>
    </ul>
</div>'''
    }
    return benefits.get(category, benefits['General'])

def generate_faq_section(category):
    """Generate FAQ section based on tool category"""
    faqs = {
        'Image': '''
<div class="tool-faqs">
    <h3>Frequently Asked Questions</h3>
    <div class="faq-item">
        <h4>What image formats are supported?</h4>
        <p>Our tool supports all major image formats including JPEG, PNG, WebP, GIF, BMP, and TIFF.</p>
    </div>
    <div class="faq-item">
        <h4>Will my image quality be reduced?</h4>
        <p>We use advanced algorithms to maintain image quality while optimizing size. You can adjust quality settings for the best balance.</p>
    </div>
    <div class="faq-item">
        <h4>Is there a file size limit?</h4>
        <p>File size limits vary by tool, but most support images up to 10MB. For larger files, consider using our compression tool first.</p>
    </div>
    <div class="faq-item">
        <h4>Are my images stored on your server?</h4>
        <p>No, all processing happens locally in your browser. Your images are never uploaded to our servers.</p>
    </div>
</div>''',
        'Encryption': '''
<div class="tool-faqs">
    <h3>Frequently Asked Questions</h3>
    <div class="faq-item">
        <h4>Is the encryption secure?</h4>
        <p>Yes, we use industry-standard encryption algorithms. However, for highly sensitive data, we recommend using offline tools.</p>
    </div>
    <div class="faq-item">
        <h4>What happens to my data?</h4>
        <p>All processing happens locally in your browser. Your data is not stored or transmitted to our servers.</p>
    </div>
    <div class="faq-item">
        <h4>Can I decrypt data encrypted elsewhere?</h4>
        <p>Yes, as long as you use the same algorithm and key that was used for encryption.</p>
    </div>
    <div class="faq-item">
        <h4>Are there any usage limitations?</h4>
        <p>No, you can use our encryption tools as much as you need completely free of charge.</p>
    </div>
</div>''',
        'Code': '''
<div class="tool-faqs">
    <h3>Frequently Asked Questions</h3>
    <div class="faq-item">
        <h4>What programming languages are supported?</h4>
        <p>Our code tools support all major languages including JavaScript, HTML, CSS, Python, Java, C/C++, PHP, Ruby, and many more.</p>
    </div>
    <div class="faq-item">
        <h4>Is my code stored anywhere?</h4>
        <p>No, all processing happens locally in your browser. Your code is never sent to our servers.</p>
    </div>
    <div class="faq-item">
        <h4>Can I customize the formatting rules?</h4>
        <p>Yes, most of our code tools offer customizable formatting options to match your preferred coding style.</p>
    </div>
    <div class="faq-item">
        <h4>What if my code is very large?</h4>
        <p>Our tools can handle large code files, but performance may vary depending on your browser and device capabilities.</p>
    </div>
</div>''',
        'Network': '''
<div class="tool-faqs">
    <h3>Frequently Asked Questions</h3>
    <div class="faq-item">
        <h4>How accurate is the network information?</h4>
        <p>We use reliable databases and APIs to provide accurate information, but some data (especially geolocation) may not always be 100% precise.</p>
    </div>
    <div class="faq-item">
        <h4>Why does it take time to process some network requests?</h4>
        <p>Some network tools need to query external services or perform multiple checks, which can take longer depending on network conditions.</p>
    </div>
    <div class="faq-item">
        <h4>Can I use these tools to test any website?</h4>
        <p>Yes, you can use our network tools to analyze any publicly accessible website or IP address.</p>
    </div>
    <div class="faq-item">
        <h4>Are there any usage limits?</h4>
        <p>We may impose reasonable usage limits to prevent abuse, but normal usage for individuals is completely free.</p>
    </div>
</div>''',
        'General': '''
<div class="tool-faqs">
    <h3>Frequently Asked Questions</h3>
    <div class="faq-item">
        <h4>Do I need to register to use this tool?</h4>
        <p>No registration is required. All our tools are available for free without any sign-up process.</p>
    </div>
    <div class="faq-item">
        <h4>Is there a mobile version available?</h4>
        <p>Yes, all our tools are fully responsive and work well on mobile devices and tablets.</p>
    </div>
    <div class="faq-item">
        <h4>Can I use these tools commercially?</h4>
        <p>Yes, our tools are free for both personal and commercial use.</p>
    </div>
    <div class="faq-item">
        <h4>What browsers are supported?</h4>
        <p>Our tools work on all modern browsers including Chrome, Firefox, Safari, Edge, and Opera.</p>
    </div>
</div>'''
    }
    return faqs.get(category, faqs['General'])

def generate_related_tools(category):
    """Generate related tools section based on category"""
    related_tools = {
        'Image': '''
<div class="related-tools">
    <h3>Related Tools</h3>
    <div class="tool-grid">
        <a href="../tools/image-compressor.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">📷</div>
                <h4>Image Compressor</h4>
                <p>Reduce image file size without losing quality</p>
            </div>
        </a>
        <a href="../tools/image-converter.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">🔄</div>
                <h4>Image Converter</h4>
                <p>Convert images between different formats</p>
            </div>
        </a>
        <a href="../tools/image-cropper.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">✂️</div>
                <h4>Image Cropper</h4>
                <p>Crop and resize images to any dimension</p>
            </div>
        </a>
    </div>
</div>''',
        'Encryption': '''
<div class="related-tools">
    <h3>Related Tools</h3>
    <div class="tool-grid">
        <a href="../tools/base64-encoder.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">🔒</div>
                <h4>Base64 Encoder</h4>
                <p>Encode and decode Base64 strings</p>
            </div>
        </a>
        <a href="../tools/md5-encryption.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">🔐</div>
                <h4>MD5 Hash Generator</h4>
                <p>Generate MD5 hashes of your data</p>
            </div>
        </a>
        <a href="../tools/sha-encryption.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">🛡️</div>
                <h4>SHA Encryption</h4>
                <p>Generate SHA-1, SHA-256, and SHA-512 hashes</p>
            </div>
        </a>
    </div>
</div>''',
        'Code': '''
<div class="related-tools">
    <h3>Related Tools</h3>
    <div class="tool-grid">
        <a href="../tools/js-minify-format.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">⚙️</div>
                <h4>JavaScript Minifier</h4>
                <p>Minify and compress JavaScript code</p>
            </div>
        </a>
        <a href="../tools/json-formatter.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">📋</div>
                <h4>JSON Formatter</h4>
                <p>Format and validate JSON data</p>
            </div>
        </a>
        <a href="../tools/html-minify-format.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">🌐</div>
                <h4>HTML Minifier</h4>
                <p>Minify HTML code for web optimization</p>
            </div>
        </a>
    </div>
</div>''',
        'Network': '''
<div class="related-tools">
    <h3>Related Tools</h3>
    <div class="tool-grid">
        <a href="../tools/ip-lookup.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">🌍</div>
                <h4>IP Lookup</h4>
                <p>Get geolocation information for any IP address</p>
            </div>
        </a>
        <a href="../tools/dns-lookup.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">🔍</div>
                <h4>DNS Lookup</h4>
                <p>Find DNS records for any domain</p>
            </div>
        </a>
        <a href="../tools/ping-test.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">📡</div>
                <h4>Ping Test</h4>
                <p>Check connectivity and response time</p>
            </div>
        </a>
    </div>
</div>''',
        'General': '''
<div class="related-tools">
    <h3>Related Tools</h3>
    <div class="tool-grid">
        <a href="../index.html" class="tool-card-link">
            <div class="tool-card">
                <div class="tool-icon">🏠</div>
                <h4>All Tools</h4>
                <p>Explore all our free online tools</p>
            </div>
        </a>
    </div>
</div>'''
    }
    return related_tools.get(category, related_tools['General'])

def add_css_for_enhanced_content():
    """Generate CSS for the enhanced content sections"""
    return '''
    <style>
        .tool-container {
            margin-bottom: 40px;
        }
        
        .how-to-use,
        .tool-benefits,
        .tool-faqs,
        .related-tools {
            background: #f9f9f9;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        
        .how-to-use h3,
        .tool-benefits h3,
        .tool-faqs h3,
        .related-tools h3 {
            color: #333;
            margin-top: 0;
            margin-bottom: 20px;
            font-size: 22px;
            border-bottom: 2px solid #eaeaea;
            padding-bottom: 10px;
        }
        
        .how-to-use ol,
        .tool-benefits ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .how-to-use li,
        .tool-benefits li {
            margin-bottom: 10px;
            line-height: 1.6;
        }
        
        .how-to-use strong {
            color: #1E88E5;
        }
        
        .faq-item {
            margin-bottom: 20px;
            border-bottom: 1px solid #eaeaea;
            padding-bottom: 15px;
        }
        
        .faq-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .faq-item h4 {
            margin-top: 0;
            margin-bottom: 8px;
            color: #333;
            font-size: 18px;
        }
        
        .faq-item p {
            margin: 0;
            color: #666;
            line-height: 1.6;
        }
        
        .tool-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .tool-card {
            background: #fff;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .tool-icon {
            font-size: 40px;
            margin-bottom: 15px;
        }
        
        .tool-card h4 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 18px;
        }
        
        .tool-card p {
            margin: 0;
            color: #666;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .tool-grid {
                grid-template-columns: 1fr;
            }
            
            .how-to-use,
            .tool-benefits,
            .tool-faqs,
            .related-tools {
                padding: 20px;
            }
        }
    </style>
    '''

def enhance_tool_page_content(file_path):
    """Enhance content of a tool page"""
    filename = os.path.basename(file_path)
    
    # Skip non-HTML files and main pages
    if not filename.endswith('.html') or filename in ['index.html', 'encry.html', 'code.html', 'network.html', 'dav.html']:
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if content is already enhanced
    if 'tool-faqs' in content or 'how-to-use' in content:
        print(f"Content already enhanced in {filename}")
        return False
    
    # Get tool information
    tool_name = get_tool_name(filename)
    category = get_tool_category(filename)
    
    # Generate enhanced content
    css = add_css_for_enhanced_content()
    usage_guide = generate_usage_guide(category)
    benefits_section = generate_benefits_section(category, tool_name)
    faq_section = generate_faq_section(category)
    related_tools = generate_related_tools(category)
    
    # Combine all enhanced content
    enhanced_content = css + usage_guide + benefits_section + faq_section + related_tools
    
    # Insert enhanced content before closing body tag
    updated_content = re.sub(r'</body>', enhanced_content + '\n</body>', content)
    
    # Write updated content back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Enhanced content for {filename}")
    return True

def enhance_all_tool_pages():
    """Enhance content for all tool pages"""
    tools_dir = '/Users/macbookpro/Desktop/trae/oopenai2026/tools'
    count = 0
    
    if os.path.exists(tools_dir):
        for filename in os.listdir(tools_dir):
            file_path = os.path.join(tools_dir, filename)
            if enhance_tool_page_content(file_path):
                count += 1
    
    print(f"Total pages with enhanced content: {count}")

if __name__ == "__main__":
    enhance_all_tool_pages()