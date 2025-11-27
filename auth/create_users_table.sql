-- 创建 users 表用于存储用户信息
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    provider TEXT DEFAULT 'google',
    last_sign_in TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_last_sign_in ON public.users(last_sign_in);

-- 启用行级安全策略 (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- 创建策略：用户只能查看和更新自己的数据
CREATE POLICY "Users can view own data"
    ON public.users
    FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own data"
    ON public.users
    FOR UPDATE
    USING (auth.uid() = id);

-- 创建策略：允许插入新用户（由认证系统触发）
CREATE POLICY "Enable insert for authenticated users"
    ON public.users
    FOR INSERT
    WITH CHECK (auth.uid() = id);

-- 创建函数：自动更新 updated_at 字段
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器：在更新时自动更新 updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 添加注释
COMMENT ON TABLE public.users IS '存储用户基本信息和登录记录';
COMMENT ON COLUMN public.users.id IS '用户ID，关联 auth.users';
COMMENT ON COLUMN public.users.email IS '用户邮箱';
COMMENT ON COLUMN public.users.full_name IS '用户全名';
COMMENT ON COLUMN public.users.avatar_url IS '用户头像URL';
COMMENT ON COLUMN public.users.provider IS '登录提供商（google, github等）';
COMMENT ON COLUMN public.users.last_sign_in IS '最后登录时间';
COMMENT ON COLUMN public.users.created_at IS '账户创建时间';
COMMENT ON COLUMN public.users.updated_at IS '最后更新时间';
