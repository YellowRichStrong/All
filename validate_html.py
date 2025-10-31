import re

# Simple HTML validation to check for common errors
def validate_html(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    errors = []
    
    # Check for unclosed tags
    tag_pattern = r'<(\w+)([^>]*)>'
    end_tag_pattern = r'</(\w+)>'
    
    opening_tags = []
    for match in re.finditer(tag_pattern, content):
        tag_name = match.group(1).lower()
        # Skip self-closing tags
        if not re.search(r'\s*/\s*>$', match.group(2)) and tag_name not in ['br', 'hr', 'img', 'input', 'meta', 'link']:
            opening_tags.append(tag_name)
    
    for match in re.finditer(end_tag_pattern, content):
        tag_name = match.group(1).lower()
        if opening_tags and opening_tags[-1] == tag_name:
            opening_tags.pop()
    
    if opening_tags:
        errors.append(f"Unclosed tags: {', '.join(opening_tags)}")
    
    # Check for JavaScript errors like missing arguments
    js_errors = re.finditer(r'\.replace\(\s*\)', content)
    for error in js_errors:
        errors.append(f"Missing arguments in replace() at position {error.start()}")
    
    # Check for invalid syntax in if statements
    if_errors = re.finditer(r'if\s*\(\s*\)', content)
    for error in if_errors:
        errors.append(f"Empty condition in if statement at position {error.start()}")
    
    return errors

# Validate the file
errors = validate_html('/Users/macbookpro/Desktop/trae/oopenai2026/tools/html-minify-format.html')
print(f"Validation completed for html-minify-format.html")
if errors:
    for error in errors:
        print(f"Error: {error}")
else:
    print("No errors found")