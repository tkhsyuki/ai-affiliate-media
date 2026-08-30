import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { MDXRemote } from 'next-mdx-remote/rsc';
import { getAllPostSlugs, getPostBySlug } from '@/lib/mdx';
import AffiliateBlock from '@/components/AffiliateBlock';

interface Props {
  params: Promise<{ slug: string }>;
}

/** 全スラッグを事前生成 (SSG) */
export async function generateStaticParams() {
  const slugs = getAllPostSlugs();
  return slugs.map((slug) => ({ slug }));
}

/** OGP メタデータを動的生成 */
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) return {};

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.date,
      images: [{ url: post.thumbnail, width: 800, height: 400, alt: post.title }],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.thumbnail],
    },
  };
}

/** アフィリエイトプレースホルダーをコンポーネントに置換 */
function preprocessContent(content: string): string {
  return content
    .replace(/<!-- AFFILIATE_AMAZON -->/g, '<AffiliateAmazon />')
    .replace(/<!-- AFFILIATE_A8 -->/g, '<AffiliateA8 />')
    .replace(/<!-- AFFILIATE_NOTION -->/g, '<AffiliateNotion />');
}

/** MDX カスタムコンポーネント */
const mdxComponents = {
  AffiliateAmazon: () => <AffiliateBlock type="amazon" />,
  AffiliateA8: () => <AffiliateBlock type="a8" />,
  AffiliateNotion: () => <AffiliateBlock type="notion" />,
};

export default async function PostPage({ params }: Props) {
  const { slug } = await params;
  const post = getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  const processedContent = preprocessContent(post.content);

  return (
    <article className="max-w-3xl mx-auto">
      {/* パンくずリスト */}
      <nav className="text-sm text-slate-500 mb-6 flex items-center gap-2">
        <Link href="/" className="hover:text-brand-600 transition-colors">
          ホーム
        </Link>
        <span>/</span>
        <span className="text-slate-700 line-clamp-1">{post.title}</span>
      </nav>

      {/* タグ */}
      {post.tags && post.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {post.tags.map((tag) => (
            <span
              key={tag}
              className="inline-block px-3 py-1 text-xs font-medium bg-blue-50 text-blue-700 rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* タイトル */}
      <h1 className="text-2xl md:text-3xl font-bold text-slate-800 leading-tight mb-4">
        {post.title}
      </h1>

      {/* 日付 */}
      <div className="flex items-center gap-2 text-sm text-slate-400 mb-6">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <time dateTime={post.date}>公開日: {post.date}</time>
      </div>

      {/* サムネイル */}
      <div className="relative w-full aspect-video rounded-xl overflow-hidden mb-8 bg-slate-100">
        <Image
          src={post.thumbnail}
          alt={post.title}
          fill
          priority
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 800px"
        />
      </div>

      {/* 記事本文 */}
      <div className="prose prose-slate prose-base md:prose-lg max-w-none
        prose-headings:font-bold prose-headings:text-slate-800
        prose-a:text-brand-600 prose-a:no-underline hover:prose-a:underline
        prose-img:rounded-lg prose-code:bg-slate-100 prose-code:px-1 prose-code:rounded">
        <MDXRemote source={processedContent} components={mdxComponents} />
      </div>

      {/* 記事下部ナビ */}
      <div className="mt-12 pt-8 border-t border-slate-200">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-brand-600 hover:text-brand-700 font-medium transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          記事一覧に戻る
        </Link>
      </div>
    </article>
  );
}
