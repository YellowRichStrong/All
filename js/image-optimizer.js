/**
 * NBA11壁纸网站图片优化库
 * 提供图片懒加载、响应式图片、WebP格式支持等功能
 */

class ImageOptimizer {
    constructor(options = {}) {
        this.options = {
            lazyLoad: true,
            useWebP: true,
            quality: 0.85,
            maxWidth: 1920,
            maxHeight: 1080,
            placeholderColor: '#f0f0f0',
            ...options
        };
        
        this.observer = null;
        this.init();
    }
    
    init() {
        if (this.options.lazyLoad) {
            this.initLazyLoading();
        }
        
        if (this.options.useWebP) {
            this.initWebPSupport();
        }
    }
    
    /**
     * 初始化图片懒加载
     */
    initLazyLoading() {
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        this.observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.1
            });
            
            // 观察所有懒加载图片
            document.querySelectorAll('img[data-src]').forEach(img => {
                this.observer.observe(img);
            });
        } else {
            // 降级方案：直接加载所有图片
            document.querySelectorAll('img[data-src]').forEach(img => {
                this.loadImage(img);
            });
        }
    }
    
    /**
     * 加载单个图片
     */
    loadImage(img) {
        const src = img.dataset.src;
        if (!src) return;
        
        // 创建新的Image对象预加载
        const tempImg = new Image();
        tempImg.onload = () => {
            img.src = src;
            img.classList.remove('lazy');
            img.classList.add('loaded');
            
            // 触发加载完成事件
            img.dispatchEvent(new CustomEvent('imageLoaded', {
                detail: { src }
            }));
        };
        
        tempImg.onerror = () => {
            console.error('图片加载失败:', src);
            img.classList.add('load-error');
        };
        
        tempImg.src = src;
    }
    
    /**
     * 初始化WebP格式支持检测
     */
    initWebPSupport() {
        // 检测浏览器是否支持WebP
        this.supportsWebP = this.checkWebPSupport();
        
        if (this.supportsWebP) {
            document.documentElement.classList.add('webp-supported');
        } else {
            document.documentElement.classList.add('webp-not-supported');
        }
    }
    
    /**
     * 检测WebP支持
     */
    checkWebPSupport() {
        return new Promise(resolve => {
            const webP = new Image();
            webP.onload = webP.onerror = function() {
                resolve(webP.height === 2);
            };
            webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        });
    }
    
    /**
     * 生成响应式图片URL
     */
    generateResponsiveSrcset(baseUrl, sizes = [320, 640, 1024, 1920]) {
        if (!this.supportsWebP) {
            return sizes.map(size => `${baseUrl}?width=${size} ${size}w`).join(', ');
        }
        
        return sizes.map(size => {
            const webpUrl = baseUrl.replace(/\.(jpg|jpeg|png)$/, '.webp');
            return `${webpUrl}?width=${size} ${size}w`;
        }).join(', ');
    }
    
    /**
     * 压缩图片
     */
    async compressImage(file, options = {}) {
        const config = { ...this.options, ...options };
        
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    // 计算缩放后的尺寸
                    let { width, height } = this.calculateDimensions(
                        img.width, 
                        img.height, 
                        config.maxWidth, 
                        config.maxHeight
                    );
                    
                    canvas.width = width;
                    canvas.height = height;
                    
                    // 高质量缩放
                    ctx.imageSmoothingEnabled = true;
                    ctx.imageSmoothingQuality = 'high';
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    // 选择输出格式
                    const mimeType = config.useWebP ? 'image/webp' : file.type;
                    
                    canvas.toBlob(
                        blob => {
                            if (blob) {
                                resolve({
                                    blob,
                                    width,
                                    height,
                                    originalSize: file.size,
                                    compressedSize: blob.size,
                                    reduction: ((1 - blob.size / file.size) * 100).toFixed(1)
                                });
                            } else {
                                reject(new Error('无法创建压缩后的图片'));
                            }
                        },
                        mimeType,
                        config.quality
                    );
                };
                img.onerror = reject;
                img.src = e.target.result;
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }
    
    /**
     * 计算图片尺寸
     */
    calculateDimensions(originalWidth, originalHeight, maxWidth, maxHeight) {
        let width = originalWidth;
        let height = originalHeight;
        
        if (width > maxWidth) {
            height = (height * maxWidth) / width;
            width = maxWidth;
        }
        
        if (height > maxHeight) {
            width = (width * maxHeight) / height;
            height = maxHeight;
        }
        
        return {
            width: Math.round(width),
            height: Math.round(height)
        };
    }
    
    /**
     * 批量压缩图片
     */
    async batchCompress(files, options = {}) {
        const results = [];
        const total = files.length;
        
        for (let i = 0; i < files.length; i++) {
            try {
                const result = await this.compressImage(files[i], options);
                results.push({
                    file: files[i],
                    result,
                    progress: Math.round(((i + 1) / total) * 100)
                });
                
                // 触发进度事件
                this.dispatchProgressEvent(i + 1, total, files[i].name);
            } catch (error) {
                console.error(`压缩失败 ${files[i].name}:`, error);
                results.push({
                    file: files[i],
                    error: error.message,
                    progress: Math.round(((i + 1) / total) * 100)
                });
            }
        }
        
        return results;
    }
    
    /**
     * 创建低质量图片占位符
     */
    createLQIP(img, width = 20, quality = 0.1) {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            const aspectRatio = img.naturalHeight / img.naturalWidth;
            canvas.width = width;
            canvas.height = width * aspectRatio;
            
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
            canvas.toBlob(blob => {
                resolve(URL.createObjectURL(blob));
            }, 'image/jpeg', quality);
        });
    }
    
    /**
     * 预加载图片
     */
    preloadImages(urls) {
        return Promise.all(
            urls.map(url => 
                new Promise((resolve, reject) => {
                    const img = new Image();
                    img.onload = resolve;
                    img.onerror = reject;
                    img.src = url;
                })
            )
        );
    }
    
    /**
     * 获取图片信息
     */
    getImageInfo(url) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                resolve({
                    width: img.naturalWidth,
                    height: img.naturalHeight,
                    url: url
                });
            };
            img.onerror = reject;
            img.src = url;
        });
    }
    
    /**
     * 分发进度事件
     */
    dispatchProgressEvent(current, total, filename) {
        const event = new CustomEvent('imageCompressProgress', {
            detail: {
                current,
                total,
                progress: Math.round((current / total) * 100),
                filename
            }
        });
        document.dispatchEvent(event);
    }
    
    /**
     * 销毁实例
     */
    destroy() {
        if (this.observer) {
            this.observer.disconnect();
        }
    }
}

// 全局工具函数
const ImageUtils = {
    /**
     * 格式化文件大小
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    /**
     * 生成图片URL
     */
    generateImageUrl(baseUrl, params = {}) {
        const url = new URL(baseUrl, window.location.origin);
        Object.keys(params).forEach(key => {
            url.searchParams.set(key, params[key]);
        });
        return url.toString();
    },
    
    /**
     * 检测图片是否加载完成
     */
    isImageLoaded(img) {
        return img.complete && img.naturalHeight !== 0;
    },
    
    /**
     * 创建图片加载器
     */
    createImageLoader() {
        const loader = document.createElement('div');
        loader.className = 'image-loader';
        loader.innerHTML = `
            <div class="loader-spinner"></div>
            <div class="loader-text">加载中...</div>
        `;
        return loader;
    },
    
    /**
     * 显示通知
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // 自动隐藏
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
        
        // 手动关闭
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        });
    }
};

// 导出到全局作用域
window.ImageOptimizer = ImageOptimizer;
window.ImageUtils = ImageUtils;

// 自动初始化
document.addEventListener('DOMContentLoaded', function() {
    // 自动初始化图片优化器
    if (typeof window.imageOptimizer === 'undefined') {
        window.imageOptimizer = new ImageOptimizer();
    }
    
    // 为所有图片添加加载状态
    document.querySelectorAll('img').forEach(img => {
        if (!img.complete) {
            img.classList.add('loading');
            
            img.addEventListener('load', function() {
                this.classList.remove('loading');
                this.classList.add('loaded');
            });
            
            img.addEventListener('error', function() {
                this.classList.remove('loading');
                this.classList.add('load-error');
            });
        } else {
            img.classList.add('loaded');
        }
    });
});

// 样式
const styles = `
.image-loader {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 10;
}

.loader-spinner {
    width: 30px;
    height: 30px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #0066cc;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 10px;
}

.loader-text {
    font-size: 12px;
    color: #666;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

img.loading {
    opacity: 0.5;
}

img.loaded {
    opacity: 1;
    transition: opacity 0.3s ease;
}

img.load-error {
    opacity: 0.3;
    background-color: #f8f9fa;
}

.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    max-width: 300px;
    animation: slideIn 0.3s ease;
}

.notification-content {
    padding: 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.notification-message {
    flex: 1;
    margin-right: 10px;
}

.notification-close {
    background: none;
    border: none;
    font-size: 18px;
    cursor: pointer;
    color: #666;
}

.notification.fade-out {
    animation: slideOut 0.3s ease forwards;
}

.notification-info {
    border-left: 4px solid #0066cc;
}

.notification-success {
    border-left: 4px solid #28a745;
}

.notification-warning {
    border-left: 4px solid #ffc107;
}

.notification-error {
    border-left: 4px solid #dc3545;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOut {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

.webp-supported .webp-fallback {
    display: none;
}

.webp-not-supported .webp-image {
    display: none;
}
`;

// 注入样式
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);
