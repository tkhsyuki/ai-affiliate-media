"""RSS フィード取得ユーティリティ"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

import feedparser
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

# 取得対象の RSS フィード一覧
RSS_FEEDS: list[dict[str, str]] = [
    {
        "url": "https://zenn.dev/topics/ai/feed",
        "source": "zenn_ai",
        "label": "Zenn AI トピック",
    },
    {
        "url": "https://zenn.dev/topics/llm/feed",
        "source": "zenn_llm",
        "label": "Zenn LLM トピック",
    },
    {
        "url": "https://qiita.com/tags/ai/feed",
        "source": "qiita_ai",
        "label": "Qiita AI タグ",
    },
    {
        "url": "https://the-decoder.com/feed/",
        "source": "the_decoder",
        "label": "The Decoder",
    },
]


def _strip_html(text: str) -> str:
    """HTML タグを除去してプレーンテキストを返す"""
    if not text:
        return ""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def _parse_date(entry: Any) -> str:
    """feedparser のエントリから ISO 8601 日時文字列を返す"""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return dt.isoformat()
    return datetime.now(timezone.utc).isoformat()


def _fetch_single_feed(feed_info: dict[str, str]) -> list[dict[str, str]]:
    """1 つの RSS フィードを取得して記事リストを返す"""
    url = feed_info["url"]
    source = feed_info["source"]
    label = feed_info["label"]

    try:
        console.print(f"[cyan]取得中:[/cyan] {label} ({url})")
        parsed = feedparser.parse(url)

        if parsed.bozo and not parsed.entries:
            console.print(f"[yellow]警告:[/yellow] {label} の取得に失敗しました（スキップ）")
            return []

        articles: list[dict[str, str]] = []
        for entry in parsed.entries[:10]:  # 各フィードから最大 10 件
            title = _strip_html(getattr(entry, "title", ""))
            summary_raw = getattr(entry, "summary", "") or getattr(entry, "description", "")
            summary = _strip_html(summary_raw)[:300]
            url_entry = getattr(entry, "link", "")
            published_at = _parse_date(entry)

            if not title or not url_entry:
                continue

            articles.append(
                {
                    "title": title,
                    "summary": summary,
                    "url": url_entry,
                    "published_at": published_at,
                    "source": source,
                }
            )

        console.print(f"[green]完了:[/green] {label} — {len(articles)} 件取得")
        return articles

    except Exception as exc:
        console.print(f"[red]エラー:[/red] {label} の取得中に例外が発生しました: {exc}（スキップ）")
        return []


def fetch_all_feeds() -> list[dict[str, str]]:
    """全 RSS フィードを順番に取得し、記事リストを統合して返す"""
    all_articles: list[dict[str, str]] = []

    for feed_info in RSS_FEEDS:
        articles = _fetch_single_feed(feed_info)
        all_articles.extend(articles)
        time.sleep(0.5)  # サーバー負荷軽減

    console.print(f"[bold green]RSS 取得完了:[/bold green] 合計 {len(all_articles)} 件")
    return all_articles
