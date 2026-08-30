import Image from 'next/image';
import Link from 'next/link';
import type { PostMeta } from '@/lib/mdx';

interface Props {
  post: PostMeta;
}

export default function ArticleCard({ post }: Props) {
  return (
    <Link
      href={`/posts/${post.slug}`}
      className="group block bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden border border-slate-100"
    >
      {/* サムネイル */}
      <div className="relative aspect-video w-full overflow-hidden bg-slate-100">
        <Image
          src={post.thumbnail}
          alt={post.title}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>

      {/* コンテンツ */}
      <div className="p-5">
        {/* タグ */}
        {post.tags && post.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {post.tags.slice(0, 2).map((tag) => (
              <span
                key={tag}
                className="inline-block px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* タイトル */}
        <h2 className="text-base font-bold text-slate-800 line-clamp-2 group-hover:text-brand-600 transition-colors leading-snug mb-2">
          {post.title}
        </h2>

        {/* 概要 */}
        {post.excerpt && (
          <p className="text-sm text-slate-500 line-clamp-3 leading-relaxed mb-3">
            {post.excerpt}
          </p>
        )}

        {/* 日付 */}
        <div className="flex items-center gap-1 text-xs text-slate-400">
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <time dateTime={post.date}>{post.date}</time>
        </div>
      </div>
    </Link>
  );
}
