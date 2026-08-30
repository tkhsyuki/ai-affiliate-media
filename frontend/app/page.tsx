import { getAllPosts } from '@/lib/mdx';
import ArticleCard from '@/components/ArticleCard';

export const revalidate = 3600; // 1時間キャッシュ

export default function HomePage() {
  const posts = getAllPosts();

  return (
    <div>
      {/* ヒーロー */}
      <section className="text-center py-12 mb-10">
        <div className="inline-flex items-center gap-2 bg-blue-50 text-blue-700 px-4 py-1.5 rounded-full text-sm font-medium mb-4">
          <span>🚀</span>
          <span>毎日自動更新</span>
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-slate-800 mb-4 leading-tight">
          最新AI ツール情報を
          <br className="sm:hidden" />
          まとめてチェック
        </h1>
        <p className="text-slate-500 text-base md:text-lg max-w-xl mx-auto leading-relaxed">
          ChatGPT・画像生成AI・AI議事録ツールなど、
          ビジネスに役立つ生成AI情報を毎日自動収集・解説します。
        </p>
      </section>

      {/* 記事一覧 */}
      <section id="latest">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-slate-800">📰 最新記事</h2>
          <span className="text-sm text-slate-400">{posts.length} 件</span>
        </div>

        {posts.length === 0 ? (
          <div className="text-center py-20 text-slate-400">
            <div className="text-5xl mb-4">📭</div>
            <p className="text-lg">記事がまだありません</p>
            <p className="text-sm mt-2">パイプラインを実行すると記事が自動生成されます</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {posts.map((post) => (
              <ArticleCard key={post.slug} post={post} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
