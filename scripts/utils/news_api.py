"""NewsData.io API クライアント"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from rich.console import Console

console = Console()

NEWSDATA_BASE_URL = "https://newsdata.io/api/1/news"
MOCK_FIXTURE_PATH = Path(__file__).parent.parent / "tests" / "fixtures" / "newsdata_mock.json"


def _normalize_article(result: dict[str, Any]) -> dict[str, str]:
    """API レスポンスの1件を正規化した辞書に変換する"""
    title = result.get("title", "")
    description = result.get("description") or result.get("content", "")
    if description:
        description = description[:300]
    link = result.get("link", "")

    # 日時の正規化
    pub_date_str = result.get("pubDate", "")
    try:
        pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d %H:%M:%S")
        pub_date = pub_date.replace(tzinfo=timezone.utc)
        published_at = pub_date.isoformat()
    except (ValueError, TypeError):
        published_at = datetime.now(timezone.utc).isoformat()

    return {
        "title": title,
        "summary": description,
        "url": link,
        "published_at": published_at,
        "source": "newsdata",
    }


def fetch_news(api_key: str, max_results: int = 10) -> list[dict[str, str]]:
    """
    NewsData.io からニュース記事を取得する。
    api_key が "test" の場合はモックデータを返す。
    """
    # テスト用モック
    if api_key == "test":
        console.print("[yellow]NewsData.io:[/yellow] テストモード（モックデータを使用）")
        if MOCK_FIXTURE_PATH.exists():
            with open(MOCK_FIXTURE_PATH, encoding="utf-8") as f:
                mock_data = json.load(f)
            results = mock_data.get("results", [])[:max_results]
            articles = [_normalize_article(r) for r in results if r.get("title") and r.get("link")]
            console.print(f"[green]完了:[/green] NewsData.io モック — {len(articles)} 件")
            return articles
        return []

    # 本番 API 呼び出し
    params = {
        "apikey": api_key,
        "q": "AI OR 生成AI OR ChatGPT OR LLM",
        "language": "ja,en",
        "category": "technology",
        "size": max_results,
    }

    try:
        console.print("[cyan]取得中:[/cyan] NewsData.io API")
        with httpx.Client(timeout=30.0) as client:
            response = client.get(NEWSDATA_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        results = data.get("results", [])
        articles = [_normalize_article(r) for r in results if r.get("title") and r.get("link")]
        console.print(f"[green]完了:[/green] NewsData.io — {len(articles)} 件取得")
        return articles

    except httpx.HTTPStatusError as exc:
        console.print(f"[red]エラー:[/red] NewsData.io HTTP エラー {exc.response.status_code}（スキップ）")
        return []
    except Exception as exc:
        console.print(f"[red]エラー:[/red] NewsData.io 取得中に例外: {exc}（スキップ）")
        return []
