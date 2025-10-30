const fs = require('fs');
const path = require('path');

// List of remaining tools to create
const tools = [
    { id: 'json-get-converter', title: 'JSON/GET Request Converter', icon: '🔄', description: 'Convert JSON to GET parameters and vice versa.' },
    { id: 'js-debugger', title: 'JS Code Debugging Tool', icon: '🐞', description: 'Debug your JavaScript code in the browser.' },
    { id: 'js-minify-format', title: 'JS Minify/Format', icon: '⚡', description: 'Minify or format your JavaScript code.' },
    { id: 'color-converter', title: 'RGB/HEX Color Converter', icon: '🌈', description: 'Convert between RGB and HEX color formats.' },
    { id: 'text-binary-converter', title: 'Text/Binary Converter', icon: '0️⃣1️⃣', description: 'Convert text to binary and binary to text.' },
    { id: 'html-preview', title: 'HTML Preview', icon: '👁️', description: 'Preview HTML code in real-time.' },
    { id: 'xml-minify-format', title: 'XML Minify/Format', icon: '📝', description: 'Minify or format your XML code.' },
    { id: 'data-size-converter', title: 'Data Size Converter', icon: '📊', description: 'Convert between different data size units.' },
    { id: 'pinyin-converter', title: 'Chinese to Pinyin', icon: '🔤', description: 'Convert Chinese characters to pinyin.' },
    { id: 'sql-minify-format', title: 'SQL Minify/Format', icon: '🗄️', description: 'Minify or format your SQL queries.' },
    { id: 'timestamp-converter', title: 'Unix Timestamp Converter', icon: '⏰', description: 'Convert between Unix timestamp and date.' },
    { id: 'regex-tester', title: 'Regex Tester', icon: '🔍', description: 'Test and validate regular expressions.' },
    { id: 'json-compressor', title: 'JSON Compressor/Formatter', icon: '🗜️', description: 'Compress or format JSON data.' },
    { id: 'time-diff-calculator', title: 'Time Difference Calculator', icon: '⏱️', description: 'Calculate time differences between dates.' },
    { id: 'html-minify-format', title: 'HTML Minify/Format', icon: '📄', description: 'Minify or format your HTML code.' },
    { id: 'base-converter', title: 'Base Converter', icon: '🔢', description: 'Convert numbers between different bases.' },
    { id: 'word-counter', title: 'Word Counter', icon: '📈', description: 'Count words, characters and lines.' },
    { id: 'xml-json-converter', title: 'XML/JSON Converter', icon: '🔄', description: 'Convert between XML and JSON formats.' },
    { id: 'string-comparison', title: 'String Comparison', icon: '⚖️', description: 'Compare two strings and find differences.' }
];

// Template for tool pages
function generateToolPage(tool) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${tool.title} - OOPEN AII</title>
    <meta name="description" content="Free online ${tool.title.toLowerCase()} tool to ${tool.description.toLowerCase()}">
    <meta name="keywords" content="${tool.title.toLowerCase().replace(/ /g, '-')}, online ${tool.title.toLowerCase().replace(/ /g, '-')}, ${tool.title.toLowerCase()}">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="icon" href="../images/logo.svg" type="image/svg+xml">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6486368477427533"
      crossorigin="anonymous"></script>
    <style>
        .tool-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .tool-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .tool-icon-large {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .tool-description {
            color: #666;
            font-size: 18px;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .tool-content {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 30px;
            text-align: center;
        }
        
        .coming-soon {
            font-size: 24px;
            color: #f44336;
            margin-bottom: 20px;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
            text-decoration: none;
        }
        
        .btn-primary {
            background-color: #4CAF50;
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #45a049;
        }
        
        @media (max-width: 768px) {
            .tool-container {
                padding: 10px;
            }
            
            .tool-content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <div class="container">
            <div class="logo">
                <a href="../index.html">
                    <img src="../images/logo.png" alt="OOPEN AII Logo">
                </a>
                <h1>OOPEN AII</h1>
            </div>
            <nav>
                <ul>
                    <li><a href="../index.html">Image Tools</a></li>
                    <li class="active"><a href="../dav.html">Dav</a></li>
                    <li><a href="../about.html">About</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main>
        <div class="tool-container">
            <div class="tool-header">
                <div class="tool-icon-large">${tool.icon}</div>
                <h2>${tool.title}</h2>
                <p class="tool-description">${tool.description}</p>
            </div>
            
            <div class="tool-content">
                <div class="coming-soon">🔧 Coming Soon!</div>
                <p>This tool is currently under development and will be available soon.</p>
                <p>Please check back later or explore our other tools.</p>
                <a href="../dav.html" class="btn btn-primary">Back to All Tools</a>
            </div>

            <!-- Features Section -->
            <div style="margin-top: 40px; background-color: #f9f9f9; padding: 30px; border-radius: 8px;">
                <h3>Coming Features</h3>
                <ul style="list-style-type: none; padding: 0; max-width: 600px; margin: 0 auto;">
                    <li style="padding: 8px 0; border-bottom: 1px solid #eee; text-align: left;">✨ ${tool.title} functionality</li>
                    <li style="padding: 8px 0; border-bottom: 1px solid #eee; text-align: left;">⚡ Fast and efficient processing</li>
                    <li style="padding: 8px 0; border-bottom: 1px solid #eee; text-align: left;">📋 Easy copy to clipboard functionality</li>
                    <li style="padding: 8px 0; border-bottom: 1px solid #eee; text-align: left;">💻 Works entirely in your browser</li>
                    <li style="padding: 8px 0; border-bottom: 1px solid #eee; text-align: left;">🎨 User-friendly interface</li>
                </ul>
            </div>

            <!-- Related Tools -->
            <div style="margin-top: 40px;">
                <h3>Related Tools</h3>
                <div style="display: flex; gap: 15px; flex-wrap: wrap; justify-content: center; margin-top: 20px;">
                    <a href="../dav.html" style="text-decoration: none; color: #2196F3;">View All Development Tools</a>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2024 OOPEN AII. All rights reserved.</p>
                <div class="footer-links">
                    <a href="../privacy.html">Privacy Policy</a>
                    <a href="../terms.html">Terms of Service</a>
                    <a href="../contact.html">Contact</a>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Automatically redirect after 10 seconds
        setTimeout(function() {
            window.location.href = '../dav.html';
        }, 10000);
    </script>
</body>
</html>`;
}

// Create each tool page
const toolsDir = path.join(__dirname, 'tools');

tools.forEach(tool => {
    const filePath = path.join(toolsDir, `${tool.id}.html`);
    const content = generateToolPage(tool);
    
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Created: ${filePath}`);
});

console.log('All tool pages generated successfully!');