"""OpenAI gpt-4o-mini ラッパー — 記事生成クライアント"""
from __future__ import annotations

import re
from pathlib import Path

from openai import OpenAI
from rich.console import Console

console = Console()

MOCK_ARTICLE_PATH = Path(__file__).parent.parent / "tests" / "fixtures" / "article_mock.mdx"

SYSTEM_PROMPT = """\
あなたは日本語の SEO ライターです。以下の情報を元に、日本語のブログ記事を MDX 形式で生成してください。

記事の要件:
- 1500〜2000 文字程度
- SEO を意識したタイトル（数字・年号を含む）
- 以下の構成で書く:
  1. フロントマター (title, date, tags, thumbnail, slug, excerpt, affiliate_category)
  2. 冒頭に AI 生成コンテンツ開示: 「※本記事はAIを活用して作成されています。」
  3. リード文（検索意図に応える要約、100文字程度）
  4. 「## {ツール名}とは」セクション → その直後に <!-- AFFILIATE_AMAZON -->
  5. 「## 主な機能と使い方」セクション → その直後に <!-- AFFILIATE_A8 -->
  6. 「## おすすめの使い方・活用例」セクション
  7. 「## まとめ」セクション → その直後に <!-- AFFILIATE_AMAZON -->
  8. FAQ セクション（Q&A 形式で 3 問）

フロントマター形式:
---
title: "タイトル（SEO最適化済み）"
date: "YYYY-MM-DD"
tags: ["タグ1", "タグ2", "タグ3"]
thumbnail: "https://picsum.photos/seed/{slug}/800/400"
slug: "YYYY-MM-DD-article-slug-in-english"
excerpt: "記事の要約（OGP 用、120文字以内）"
affiliate_category: "amazon|saas|notion"
---

タグは記事テーマに合った日本語タグ 3 つを付けること。
thumbnail の seed 部分は slug と同じ英単語を使うこと。
affiliate_category は記事テーマに応じて amazon/saas/notion のいずれかを選ぶこと。
"""


def generate_article(item: dict, api_key: str) -> str:
    """
    1 件のデータアイテムから SEO 記事（MDX）を生成する。
    api_key が "test" の場合はモックデータを返す。
    """
    # テスト用モック
    if api_key == "test":
        console.print("[yellow]LLM クライアント:[/yellow] テストモード（モックデータを使用）")
        if MOCK_ARTICLE_PATH.exists():
            return MOCK_ARTICLE_PATH.read_text(encoding="utf-8")
        return _fallback_article(item)

    user_message = f"""\
以下の情報を元に記事を生成してください。

タイトル: {item.get('title', '')}
要約: {item.get('summary', '')}
元記事URL: {item.get('url', '')}
公開日: {item.get('published_at', '')[:10]}
ソース: {item.get('source', '')}
"""

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        content = response.choices[0].message.content or ""
        console.print("[green]生成完了:[/green] 記事を生成しました")
        return content

    except Exception as exc:
        console.print(f"[red]エラー:[/red] 記事生成中に例外: {exc}")
        return _fallback_article(item)


def _fallback_article(item: dict) -> str:
    """API 失敗時のフォールバック MDX を返す"""
    date_str = str(item.get("published_at", ""))[:10] or "2026-08-18"
    title = item.get("title", "AI ツール情報")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower())[:40].strip("-")
    slug = f"{date_str}-{slug}"

    return f"""\
---
title: "{title}"
date: "{date_str}"
tags: ["生成AI", "AIツール", "AI情報"]
thumbnail: "https://picsum.photos/seed/{slug}/800/400"
slug: "{slug}"
excerpt: "{item.get('summary', '')[:120]}"
affiliate_category: "amazon"
---

※本記事はAIを活用して作成されています。

{item.get('summary', '')}

## このトピックについて

{item.get('title', '')}について解説します。

<!-- AFFILIATE_AMAZON -->

## 主な内容

詳細は元記事をご参照ください: {item.get('url', '')}

<!-- AFFILIATE_A8 -->

## まとめ

最新のAI情報をお届けしました。

<!-- AFFILIATE_AMAZON -->

## よくある質問

**Q: この情報はどこから取得していますか？**
A: 信頼性の高いAI関連メディアから自動収集しています。

**Q: 記事の更新頻度は？**
A: 毎日自動更新されます。

**Q: アフィリエイトリンクについて**
A: 本サイトはアフィリエイトプログラムに参加しています。
"""
