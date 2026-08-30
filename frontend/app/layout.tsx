import type { Metadata } from 'next';
import './globals.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: {
    default: 'AI Tools Journal | 生成AIツール情報メディア',
    template: '%s | AI Tools Journal',
  },
  description:
    '最新の生成AIツールを徹底比較・解説。ChatGPT、画像生成AI、AI議事録ツールなど、ビジネスに役立つAI情報を毎日お届けします。',
  openGraph: {
    type: 'website',
    locale: 'ja_JP',
    siteName: 'AI Tools Journal',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className="min-h-screen flex flex-col bg-slate-50">
        <Header />
        <main className="flex-1 w-full max-w-6xl mx-auto px-4 py-8">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
