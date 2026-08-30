export default function Footer() {
  return (
    <footer className="bg-slate-800 text-slate-300 mt-16">
      <div className="max-w-6xl mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* ロゴ・説明 */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-xl">🤖</span>
              <span className="text-white font-bold">AI Tools Journal</span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              最新の生成AIツール情報を毎日自動更新。
              ChatGPT・画像生成AI・AI議事録ツールなど、
              ビジネスに役立つAI情報をお届けします。
            </p>
          </div>

          {/* リンク */}
          <div>
            <h3 className="text-white font-semibold mb-3">メニュー</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/" className="hover:text-white transition-colors">
                  ホーム
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  プライバシーポリシー
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  お問い合わせ
                </a>
              </li>
            </ul>
          </div>

          {/* 免責事項 */}
          <div id="about">
            <h3 className="text-white font-semibold mb-3">免責事項</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              本サイトはアフィリエイトプログラムに参加しています。
              記事内のリンクから商品・サービスを購入すると、
              サイト運営者に収益が発生する場合があります。
            </p>
            <p className="text-xs text-slate-400 leading-relaxed mt-2">
              ※本サイトの記事はAIを活用して自動生成されています。
              情報の正確性については確認しておりますが、
              ご利用は自己責任でお願いいたします。
            </p>
          </div>
        </div>

        <div className="border-t border-slate-700 mt-8 pt-6 text-center text-xs text-slate-500">
          © {new Date().getFullYear()} AI Tools Journal. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
