/**
 * Supabase Google Authentication Module
 * 使用Supabase实现Google登录功能
 */

// Supabase配置
const SUPABASE_CONFIG = {
    url: 'https://nuvfdstxwxmdobipzlbf.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dmZkc3R4d3htZG9iaXB6bGJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQwMzgxNzgsImV4cCI6MjA3OTYxNDE3OH0.46-tn_DaSzJvnG5NW7PKi_EM9CMk23hD684og6SFjlw'
};

class SupabaseAuth {
    constructor() {
        this.supabase = null;
        this.currentUser = null;
        this.init();
    }

    /**
     * 初始化Supabase客户端
     */
    async init() {
        try {
            // 动态加载Supabase JS SDK
            if (typeof supabase === 'undefined') {
                await this.loadSupabaseSDK();
            }
            
            // 创建Supabase客户端
            this.supabase = supabase.createClient(
                SUPABASE_CONFIG.url,
                SUPABASE_CONFIG.anonKey
            );

            // 检查当前登录状态
            await this.checkCurrentUser();

            // 监听认证状态变化
            this.supabase.auth.onAuthStateChange((event, session) => {
                console.log('Auth state changed:', event, session);
                this.handleAuthStateChange(event, session);
            });

            console.log('Supabase Auth initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Supabase Auth:', error);
        }
    }

    /**
     * 动态加载Supabase SDK
     */
    loadSupabaseSDK() {
        return new Promise((resolve, reject) => {
            if (typeof supabase !== 'undefined') {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    /**
     * 检查当前用户登录状态
     */
    async checkCurrentUser() {
        try {
            const { data: { user } } = await this.supabase.auth.getUser();
            this.currentUser = user;
            return user;
        } catch (error) {
            console.error('Error checking current user:', error);
            return null;
        }
    }

    /**
     * Google登录
     * @param {Object} options - 登录选项
     * @returns {Promise}
     */
    async signInWithGoogle(options = {}) {
        try {
            const { data, error } = await this.supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: options.redirectTo || `${window.location.origin}/auth/callback.html`,
                    queryParams: {
                        access_type: 'offline',
                        prompt: 'consent',
                    }
                }
            });

            if (error) throw error;

            console.log('Google sign in initiated:', data);
            return { success: true, data };
        } catch (error) {
            console.error('Google sign in error:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * 退出登录
     */
    async signOut() {
        try {
            const { error } = await this.supabase.auth.signOut();
            if (error) throw error;

            this.currentUser = null;
            console.log('User signed out successfully');
            return { success: true };
        } catch (error) {
            console.error('Sign out error:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * 获取当前用户信息
     */
    getCurrentUser() {
        return this.currentUser;
    }

    /**
     * 检查用户是否已登录
     */
    isAuthenticated() {
        return this.currentUser !== null;
    }

    /**
     * 处理认证状态变化
     */
    handleAuthStateChange(event, session) {
        switch (event) {
            case 'SIGNED_IN':
                this.currentUser = session?.user || null;
                this.onSignIn(session?.user);
                break;
            case 'SIGNED_OUT':
                this.currentUser = null;
                this.onSignOut();
                break;
            case 'USER_UPDATED':
                this.currentUser = session?.user || null;
                this.onUserUpdated(session?.user);
                break;
            default:
                break;
        }
    }

    /**
     * 登录成功回调（可被覆盖）
     */
    onSignIn(user) {
        console.log('User signed in:', user);
        // 触发自定义事件
        window.dispatchEvent(new CustomEvent('supabase-auth-signin', { detail: user }));
    }

    /**
     * 退出登录回调（可被覆盖）
     */
    onSignOut() {
        console.log('User signed out');
        // 触发自定义事件
        window.dispatchEvent(new CustomEvent('supabase-auth-signout'));
    }

    /**
     * 用户信息更新回调（可被覆盖）
     */
    onUserUpdated(user) {
        console.log('User updated:', user);
        // 触发自定义事件
        window.dispatchEvent(new CustomEvent('supabase-auth-updated', { detail: user }));
    }

    /**
     * 获取用户会话
     */
    async getSession() {
        try {
            const { data: { session } } = await this.supabase.auth.getSession();
            return session;
        } catch (error) {
            console.error('Error getting session:', error);
            return null;
        }
    }

    /**
     * 刷新会话
     */
    async refreshSession() {
        try {
            const { data: { session }, error } = await this.supabase.auth.refreshSession();
            if (error) throw error;
            return session;
        } catch (error) {
            console.error('Error refreshing session:', error);
            return null;
        }
    }
}

// 创建全局实例
window.supabaseAuth = new SupabaseAuth();
