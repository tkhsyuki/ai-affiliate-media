interface Props {
  type: 'amazon' | 'a8' | 'notion';
}

const AFFILIATE_CONFIG = {
  amazon: {
    emoji: '📚',
    label: 'Amazon で関連書籍をチェック',
    description: 'AIツールの使い方をさらに深く学べる書籍をAmazonでチェック！',
    buttonText: 'Amazonで書籍を見る →',
    buttonClass: 'bg-amber-500 hover:bg-amber-600 text-white',
    href: '#',  // Amazon アソシエイトリンクを設定してください
  },
  a8: {
    emoji: '🔧',
    label: '公式サイトで詳しく見る',
    description: '無料トライアルで実際に試してみましょう！プロ向けの高機能プランも充実。',
    buttonText: '無料で試してみる →',
    buttonClass: 'bg-green-600 hover:bg-green-700 text-white',
    href: '#',  // A8.net アフィリエイトリンクを設定してください
  },
  notion: {
    emoji: '📝',
    label: 'Notion AI を試してみる',
    description: 'NotionのAI機能で文章作成・要約・翻訳を自動化。まずは無料プランから。',
    buttonText: 'Notion を無料で始める →',
    buttonClass: 'bg-slate-800 hover:bg-slate-900 text-white',
    href: '#',  // Notion アフィリエイトリンクを設定してください
  },
} as const;

export default function AffiliateBlock({ type }: Props) {
  const config = AFFILIATE_CONFIG[type];

  return (
    <div className="my-6 p-5 bg-amber-50 border border-amber-200 rounded-xl relative">
      {/* 広告バッジ */}
      <span className="absolute top-3 right-3 text-xs bg-amber-200 text-amber-800 px-2 py-0.5 rounded font-medium">
        広告
      </span>

      <div className="flex items-start gap-3">
        <span className="text-2xl flex-shrink-0">{config.emoji}</span>
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-slate-800 text-sm mb-1">{config.label}</p>
          <p className="text-xs text-slate-600 mb-3 leading-relaxed">{config.description}</p>
          <a
            href={config.href}
            target="_blank"
            rel="noopener noreferrer nofollow"
            className={`inline-flex items-center gap-1 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${config.buttonClass}`}
          >
            {config.buttonText}
          </a>
        </div>
      </div>
    </div>
  );
}
