"""Step 1: データ収集スクリプト"""
from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from utils.news_api import fetch_news
from utils.rss_fetcher import fetch_all_feeds

load_dotenv(Path(__file__).parent / ".env")

console = Console()

# raw_data ディレクトリ（scripts の2つ上がプロジェクトルート）
RAW_DATA_DIR = Path(__file__).parent.parent / "raw_data"


def deduplicate(articles: list[dict]) -> list[dict]:
    """URL の重複を除去して記事リストを返す"""
    seen_urls: set[str] = set()
    unique: list[dict] = []
    for article in articles:
        url = article.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(article)
    return unique


def main() -> list[dict]:
    """データ収集のエントリポイント。収集した記事リストを返す。"""
    console.rule("[bold blue]Step 1: データ収集開始[/bold blue]")

    newsdata_api_key = os.getenv("NEWSDATA_API_KEY", "test")

    # RSS フィード取得
    rss_articles = fetch_all_feeds()

    # NewsData.io API 取得
    news_articles = fetch_news(api_key=newsdata_api_key, max_results=10)

    # 統合・重複除去
    all_articles = rss_articles + news_articles
    unique_articles = deduplicate(all_articles)

    console.print(
        f"[bold green]収集完了:[/bold green] {len(all_articles)} 件 → 重複除去後 {len(unique_articles)} 件"
    )

    # raw_data/{date}.json に保存
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    output_path = RAW_DATA_DIR / f"{today}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_articles, f, ensure_ascii=False, indent=2)

    console.print(f"[bold green]保存完了:[/bold green] {output_path}")
    console.rule("[bold blue]Step 1: データ収集完了[/bold blue]")

    return unique_articles


if __name__ == "__main__":
    main()
