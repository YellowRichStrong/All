# Google登录集成指南

本项目已集成Supabase Google登录功能，用户可以使用Google账号登录网站。

## 📁 文件结构

```
oopenai2026/
├── js/
│   └── supabase-auth.js      # Supabase认证库
├── auth/
│   ├── login.html             # 登录页面
│   └── callback.html          # 认证回调页面
```

## 🚀 快速开始

### 1. 访问登录页面

打开浏览器访问：
```
https://openai2026.com/auth/login.html
```

### 2. 点击"Continue with Google"按钮

用户将被重定向到Google登录页面进行授权。

### 3. 授权后自动跳转

授权成功后，用户将被重定向到回调页面（`/auth/callback.html`），然后自动跳转到首页。

## 💻 在页面中集成登录功能

### 方法一：使用封装好的认证库

在您的HTML页面中引入库文件：

```html
<!-- 引入Supabase SDK -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

<!-- 引入认证库 -->
<script src="/js/supabase-auth.js"></script>

<script>
// 使用全局实例
document.getElementById('loginBtn').addEventListener('click', async () => {
    const result = await window.supabaseAuth.signInWithGoogle();
    if (result.success) {
        console.log('登录成功');
    }
});

// 退出登录
document.getElementById('logoutBtn').addEventListener('click', async () => {
    await window.supabaseAuth.signOut();
});

// 检查登录状态
if (window.supabaseAuth.isAuthenticated()) {
    const user = window.supabaseAuth.getCurrentUser();
    console.log('当前用户:', user);
}
</script>
```

### 方法二：直接使用Supabase客户端

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
const SUPABASE_URL = 'https://nuvfdstxwxmdobipzlbf.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dmZkc3R4d3htZG9iaXB6bGJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQwMzgxNzgsImV4cCI6MjA3OTYxNDE3OH0.46-tn_DaSzJvnG5NW7PKi_EM9CMk23hD684og6SFjlw';

const client = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// Google登录
async function loginWithGoogle() {
    const { data, error } = await client.auth.signInWithOAuth({
        provider: 'google',
        options: {
            redirectTo: 'https://openai2026.com/auth/callback.html'
        }
    });
}

// 获取当前用户
async function getCurrentUser() {
    const { data: { user } } = await client.auth.getUser();
    return user;
}

// 退出登录
async function logout() {
    await client.auth.signOut();
}
</script>
```

## 🔧 配置说明

### Supabase配置

```javascript
const SUPABASE_CONFIG = {
    url: 'https://nuvfdstxwxmdobipzlbf.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
};
```

### Google OAuth配置

在Supabase后台配置：
1. 登录 Supabase Dashboard
2. 进入 Authentication → Providers
3. 启用 Google Provider
4. 配置以下信息：
   - Client ID: `524383862092-tut5vno5s2gt1oeb1rkttaj6dhtk1g32.apps.googleusercontent.com`
   - Callback URL: `https://openai2026.com/auth/callback.html`

## 📝 API参考

### SupabaseAuth类

#### 方法

**signInWithGoogle(options)**
- 触发Google登录流程
- 参数：
  - `options.redirectTo`: 登录成功后的回调URL（可选）
- 返回：`Promise<{success: boolean, data?: any, error?: string}>`

**signOut()**
- 退出登录
- 返回：`Promise<{success: boolean, error?: string}>`

**getCurrentUser()**
- 获取当前登录用户
- 返回：`User | null`

**isAuthenticated()**
- 检查用户是否已登录
- 返回：`boolean`

**getSession()**
- 获取当前会话
- 返回：`Promise<Session | null>`

### 事件监听

```javascript
// 监听登录事件
window.addEventListener('supabase-auth-signin', (event) => {
    console.log('用户已登录:', event.detail);
});

// 监听退出事件
window.addEventListener('supabase-auth-signout', () => {
    console.log('用户已退出');
});

// 监听用户信息更新
window.addEventListener('supabase-auth-updated', (event) => {
    console.log('用户信息已更新:', event.detail);
});
```

## 🎨 示例：在导航栏添加登录按钮

```html
<div id="userSection">
    <!-- 未登录状态 -->
    <div id="notLoggedIn">
        <a href="/auth/login.html" class="login-btn">Sign In</a>
    </div>
    
    <!-- 已登录状态 -->
    <div id="loggedIn" style="display:none;">
        <img id="userAvatar" src="" alt="Avatar" class="user-avatar">
        <span id="userName"></span>
        <button id="logoutBtn">Sign Out</button>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="/js/supabase-auth.js"></script>
<script>
// 检查登录状态并更新UI
async function updateUserUI() {
    const user = window.supabaseAuth.getCurrentUser();
    
    if (user) {
        document.getElementById('notLoggedIn').style.display = 'none';
        document.getElementById('loggedIn').style.display = 'flex';
        document.getElementById('userName').textContent = user.email;
        document.getElementById('userAvatar').src = user.user_metadata?.avatar_url || 
            `https://ui-avatars.com/api/?name=${user.email}`;
    } else {
        document.getElementById('notLoggedIn').style.display = 'block';
        document.getElementById('loggedIn').style.display = 'none';
    }
}

// 退出登录
document.getElementById('logoutBtn').addEventListener('click', async () => {
    await window.supabaseAuth.signOut();
    updateUserUI();
});

// 监听认证状态变化
window.addEventListener('supabase-auth-signin', updateUserUI);
window.addEventListener('supabase-auth-signout', updateUserUI);

// 页面加载时更新UI
updateUserUI();
</script>
```

## 🔒 安全注意事项

1. **不要在客户端代码中暴露Service Role Key**
   - 仅使用Anon Key
   - Service Role Key只在服务器端使用

2. **配置回调URL白名单**
   - 在Supabase后台添加允许的回调URL
   - 防止恶意重定向

3. **使用HTTPS**
   - 生产环境必须使用HTTPS
   - 保护用户凭证安全

4. **会话管理**
   - Supabase会自动处理token刷新
   - 会话默认7天过期

## 🐛 故障排查

### 问题1: 登录后跳转404
- 确认回调URL配置正确
- 检查 `/auth/callback.html` 文件是否存在

### 问题2: Google登录按钮无反应
- 检查浏览器控制台错误
- 确认Supabase配置正确
- 验证Google OAuth Client ID

### 问题3: 回调页面显示错误
- 检查Supabase后台Google Provider是否启用
- 确认域名配置正确
- 查看浏览器控制台详细错误信息

## 📚 更多资源

- [Supabase Auth文档](https://supabase.com/docs/guides/auth)
- [Google OAuth文档](https://developers.google.com/identity/protocols/oauth2)
- [Supabase JS SDK](https://supabase.com/docs/reference/javascript/introduction)

## 🎯 下一步

1. 在Supabase后台配置Google Provider
2. 测试登录流程
3. 集成到现有页面
4. 自定义用户体验

---

**需要帮助？**
如果遇到问题，请检查：
1. Supabase项目配置
2. Google OAuth Client配置
3. 回调URL设置
4. 浏览器控制台错误信息
