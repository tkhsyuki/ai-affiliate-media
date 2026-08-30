import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

// content/posts ディレクトリ（frontend の親ディレクトリ配下）
const POSTS_DIR = path.join(process.cwd(), '..', 'content', 'posts');

export interface PostMeta {
  title: string;
  date: string;
  tags: string[];
  thumbnail: string;
  slug: string;
  excerpt: string;
  affiliate_category: string;
}

export interface Post extends PostMeta {
  content: string;
}

/** すべての記事スラッグを新しい順に返す */
export function getAllPostSlugs(): string[] {
  if (!fs.existsSync(POSTS_DIR)) return [];
  return fs
    .readdirSync(POSTS_DIR)
    .filter((f) => f.endsWith('.mdx') || f.endsWith('.md'))
    .map((f) => f.replace(/\.mdx?$/, ''))
    .sort()
    .reverse();
}

/** スラッグから1件の記事を返す */
export function getPostBySlug(slug: string): Post | null {
  const mdxPath = path.join(POSTS_DIR, `${slug}.mdx`);
  const mdPath = path.join(POSTS_DIR, `${slug}.md`);
  const filePath = fs.existsSync(mdxPath)
    ? mdxPath
    : fs.existsSync(mdPath)
    ? mdPath
    : null;

  if (!filePath) return null;

  const raw = fs.readFileSync(filePath, 'utf-8');
  const { data, content } = matter(raw);

  return {
    title: (data.title as string) || '',
    date: (data.date as string) || '',
    tags: (data.tags as string[]) || [],
    thumbnail: (data.thumbnail as string) || `https://picsum.photos/seed/${slug}/800/400`,
    slug,
    excerpt: (data.excerpt as string) || '',
    affiliate_category: (data.affiliate_category as string) || 'amazon',
    content,
  };
}

/** すべての記事を新しい順に返す */
export function getAllPosts(): Post[] {
  return getAllPostSlugs()
    .map((slug) => getPostBySlug(slug))
    .filter((p): p is Post => p !== null);
}
