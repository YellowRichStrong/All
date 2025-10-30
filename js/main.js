// Main JavaScript file for OOPEN AII website

// Function to handle smooth scrolling
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Function to handle file uploads
function handleFileUpload(inputElement, previewElement) {
    inputElement.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                if (previewElement.tagName === 'IMG') {
                    previewElement.src = e.target.result;
                    previewElement.style.display = 'block';
                }
            };
            
            reader.readAsDataURL(file);
        }
    });
}

// Function to handle drag and drop
function setupDragAndDrop(uploadArea, inputElement, previewElement) {
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.style.backgroundColor = '#f0f8ff';
    });

    uploadArea.addEventListener('dragleave', function() {
        uploadArea.style.backgroundColor = '#fff';
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.style.backgroundColor = '#fff';
        
        const file = e.dataTransfer.files[0];
        if (file) {
            inputElement.files = e.dataTransfer.files;
            const event = new Event('change');
            inputElement.dispatchEvent(event);
        }
    });
}

// Function to copy text to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        console.error('Failed to copy text: ', err);
        return false;
    }
}

// Function to show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '12px 20px';
    notification.style.borderRadius = '4px';
    notification.style.color = 'white';
    notification.style.fontWeight = '500';
    notification.style.zIndex = '9999';
    notification.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
    
    if (type === 'success') {
        notification.style.backgroundColor = '#28a745';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#dc3545';
    } else if (type === 'info') {
        notification.style.backgroundColor = '#17a2b8';
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.3s';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Function to generate a random ID
function generateId() {
    return '_' + Math.random().toString(36).substr(2, 9);
}

// Image processing utilities
const ImageUtils = {
    // Convert image to grayscale
    toGrayscale(imageData) {
        const data = imageData.data;
        for (let i = 0; i < data.length; i += 4) {
            const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
            data[i] = avg; // R
            data[i + 1] = avg; // G
            data[i + 2] = avg; // B
        }
        return imageData;
    },
    
    // Apply mosaic effect
    applyMosaic(imageData, blockSize) {
        const data = imageData.data;
        const width = imageData.width;
        const height = imageData.height;
        
        for (let y = 0; y < height; y += blockSize) {
            for (let x = 0; x < width; x += blockSize) {
                const pixelIndex = (y * width + x) * 4;
                const r = data[pixelIndex];
                const g = data[pixelIndex + 1];
                const b = data[pixelIndex + 2];
                
                for (let by = 0; by < blockSize && y + by < height; by++) {
                    for (let bx = 0; bx < blockSize && x + bx < width; bx++) {
                        const blockIndex = ((y + by) * width + (x + bx)) * 4;
                        data[blockIndex] = r;
                        data[blockIndex + 1] = g;
                        data[blockIndex + 2] = b;
                    }
                }
            }
        }
        return imageData;
    },
    
    // Add text watermark
    addTextWatermark(ctx, text, x, y, options = {}) {
        const { font = '20px Arial', fillStyle = 'rgba(0,0,0,0.3)', textAlign = 'center', textBaseline = 'middle' } = options;
        
        ctx.save();
        ctx.font = font;
        ctx.fillStyle = fillStyle;
        ctx.textAlign = textAlign;
        ctx.textBaseline = textBaseline;
        ctx.fillText(text, x, y);
        ctx.restore();
    },
    
    // Extract colors from image
    extractColors(imageData, numColors = 5) {
        const data = imageData.data;
        const colorMap = new Map();
        
        for (let i = 0; i < data.length; i += 4) {
            if (data[i + 3] > 128) { // Ignore transparent pixels
                const rgb = `${data[i]},${data[i + 1]},${data[i + 2]}`;
                colorMap.set(rgb, (colorMap.get(rgb) || 0) + 1);
            }
        }
        
        return Array.from(colorMap.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, numColors)
            .map(([rgb]) => {
                const [r, g, b] = rgb.split(',').map(Number);
                return {
                    rgb: `rgb(${rgb})`,
                    hex: `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`,
                    r,
                    g,
                    b
                };
            });
    }
};

// Initialize common functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current navigation link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath || 
            (currentPath.includes('/tools/') && link.getAttribute('href') === '/index.html')) {
            link.classList.add('active');
        }
    });
    
    // Make tool cards clickable if they exist
    const toolCards = document.querySelectorAll('.tool-card');
    toolCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            const href = this.getAttribute('onclick')?.match(/window\.location\.href='([^']+)'/);
            if (href && href[1]) {
                window.location.href = href[1];
            }
        });
    });
    
    // Tool Search Functionality
    const searchInput = document.getElementById('tool-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const toolCards = document.querySelectorAll('.tool-card');
            let visibleCards = 0;
            
            toolCards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const description = card.querySelector('p').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    card.style.display = 'block';
                    visibleCards++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Update filter info
            const filterInfo = document.querySelector('.filter-info');
            if (filterInfo) {
                filterInfo.textContent = `${visibleCards} tools found`;
            }
        });
    }
    
    // Category Filter Functionality
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const category = this.getAttribute('data-category');
            const toolCards = document.querySelectorAll('.tool-card');
            let visibleCards = 0;
            
            toolCards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'block';
                    visibleCards++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Update filter info
            const filterInfo = document.querySelector('.filter-info');
            if (filterInfo) {
                filterInfo.textContent = `${visibleCards} tools found`;
            }
        });
    });
    
    // Back to Top Button
    const backToTopButton = document.createElement('button');
    backToTopButton.className = 'back-to-top';
    backToTopButton.innerHTML = '↑';
    document.body.appendChild(backToTopButton);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    // Tool Card Hover Animation Enhancement
    toolCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            this.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.15)';
            this.style.transition = 'transform 0.3s, box-shadow 0.3s';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
        });
    });
});

// Export utility functions for use in other scripts
window.Utils = {
    smoothScroll,
    handleFileUpload,
    setupDragAndDrop,
    copyToClipboard,
    showNotification,
    generateId,
    ImageUtils
};