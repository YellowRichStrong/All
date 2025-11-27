-- 创建博客文章表
CREATE TABLE IF NOT EXISTS public.blog_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    excerpt TEXT NOT NULL,
    content TEXT NOT NULL,
    meta_keywords TEXT,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published')),
    author_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    author_name TEXT,
    published_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON public.blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_posts_status ON public.blog_posts(status);
CREATE INDEX IF NOT EXISTS idx_blog_posts_category ON public.blog_posts(category);
CREATE INDEX IF NOT EXISTS idx_blog_posts_author ON public.blog_posts(author_id);
CREATE INDEX IF NOT EXISTS idx_blog_posts_published_at ON public.blog_posts(published_at DESC);

-- 启用行级安全策略
ALTER TABLE public.blog_posts ENABLE ROW LEVEL SECURITY;

-- 创建策略：所有人都可以查看已发布的文章
CREATE POLICY "Anyone can view published posts"
    ON public.blog_posts
    FOR SELECT
    USING (status = 'published' OR auth.uid() = author_id);

-- 创建策略：认证用户可以创建文章
CREATE POLICY "Authenticated users can create posts"
    ON public.blog_posts
    FOR INSERT
    WITH CHECK (auth.uid() = author_id);

-- 创建策略：作者可以更新自己的文章
CREATE POLICY "Authors can update own posts"
    ON public.blog_posts
    FOR UPDATE
    USING (auth.uid() = author_id);

-- 创建策略：作者可以删除自己的文章
CREATE POLICY "Authors can delete own posts"
    ON public.blog_posts
    FOR DELETE
    USING (auth.uid() = author_id);

-- 创建触发器：自动更新 updated_at
CREATE OR REPLACE FUNCTION update_blog_posts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blog_posts_updated_at
    BEFORE UPDATE ON public.blog_posts
    FOR EACH ROW
    EXECUTE FUNCTION update_blog_posts_updated_at();

-- 添加注释
COMMENT ON TABLE public.blog_posts IS '博客文章表';
COMMENT ON COLUMN public.blog_posts.id IS '文章ID';
COMMENT ON COLUMN public.blog_posts.title IS '文章标题';
COMMENT ON COLUMN public.blog_posts.slug IS 'URL友好的文章标识';
COMMENT ON COLUMN public.blog_posts.category IS '文章分类';
COMMENT ON COLUMN public.blog_posts.excerpt IS '文章摘要';
COMMENT ON COLUMN public.blog_posts.content IS '文章内容（HTML）';
COMMENT ON COLUMN public.blog_posts.meta_keywords IS 'SEO关键词';
COMMENT ON COLUMN public.blog_posts.status IS '发布状态（draft/published）';
COMMENT ON COLUMN public.blog_posts.author_id IS '作者ID';
COMMENT ON COLUMN public.blog_posts.author_name IS '作者名字';
COMMENT ON COLUMN public.blog_posts.published_at IS '发布时间';
COMMENT ON COLUMN public.blog_posts.created_at IS '创建时间';
COMMENT ON COLUMN public.blog_posts.updated_at IS '更新时间';
