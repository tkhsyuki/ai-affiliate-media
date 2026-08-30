'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* ロゴ */}
        <Link href="/" className="flex items-center gap-2 group">
          <span className="text-2xl">🤖</span>
          <span className="text-xl font-bold text-slate-800 group-hover:text-brand-600 transition-colors">
            AI Tools Journal
          </span>
        </Link>

        {/* デスクトップナビ */}
        <nav className="hidden md:flex items-center gap-6">
          <Link
            href="/"
            className="text-sm font-medium text-slate-600 hover:text-brand-600 transition-colors"
          >
            ホーム
          </Link>
          <Link
            href="/#latest"
            className="text-sm font-medium text-slate-600 hover:text-brand-600 transition-colors"
          >
            最新記事
          </Link>
          <Link
            href="/#about"
            className="text-sm font-medium text-slate-600 hover:text-brand-600 transition-colors"
          >
            運営者情報
          </Link>
        </nav>

        {/* モバイルハンバーガー */}
        <button
          className="md:hidden p-2 rounded-md text-slate-600 hover:text-brand-600 hover:bg-slate-100"
          onClick={() => setMenuOpen((prev) => !prev)}
          aria-label="メニューを開く"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            {menuOpen ? (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            ) : (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            )}
          </svg>
        </button>
      </div>

      {/* モバイルメニュー */}
      {menuOpen && (
        <div className="md:hidden border-t border-slate-100 bg-white">
          <nav className="max-w-6xl mx-auto px-4 py-3 flex flex-col gap-3">
            <Link
              href="/"
              className="text-sm font-medium text-slate-700 py-2"
              onClick={() => setMenuOpen(false)}
            >
              ホーム
            </Link>
            <Link
              href="/#latest"
              className="text-sm font-medium text-slate-700 py-2"
              onClick={() => setMenuOpen(false)}
            >
              最新記事
            </Link>
            <Link
              href="/#about"
              className="text-sm font-medium text-slate-700 py-2"
              onClick={() => setMenuOpen(false)}
            >
              運営者情報
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
