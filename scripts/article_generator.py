"""Step 2: 記事生成スクリプト"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from utils.llm_client import generate_article

load_dotenv(Path(__file__).parent / ".env")

console = Console()

RAW_DATA_DIR = Path(__file__).parent.parent / "raw_data"
POSTS_DIR = Path(__file__).parent.parent / "content" / "posts"
MAX_ARTICLES_PER_DAY = 5  # API コスト管理


def extract_slug(mdx_content: str, fallback: str) -> str:
    """MDX フロントマターから slug を抽出する"""
    match = re.search(r'^slug:\s*["\']?([^"\'\\n]+)["\']?', mdx_content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return fallback


def main(articles: list[dict] | None = None) -> None:
    """
    記事生成のエントリポイント。
    articles が None の場合は今日の raw_data ファイルを読み込む。
    """
    console.rule("[bold blue]Step 2: 記事生成開始[/bold blue]")

    openai_api_key = os.getenv("OPENAI_API_KEY", "test")

    # 記事データの読み込み
    if articles is None:
        today = date.today().isoformat()
        raw_path = RAW_DATA_DIR / f"{today}.json"
        if not raw_path.exists():
            console.print(f"[red]エラー:[/red] {raw_path} が見つかりません。先に data_collector.py を実行してください。")
            return
        with open(raw_path, encoding="utf-8") as f:
            articles = json.load(f)

    # 最大件数に制限
    articles = articles[:MAX_ARTICLES_PER_DAY]
    console.print(f"[cyan]記事生成対象:[/cyan] {len(articles)} 件")

    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    generated_count = 0
    for i, item in enumerate(articles, 1):
        console.print(f"\n[bold]--- [{i}/{len(articles)}] {item.get('title', '')[:50]}... ---[/bold]")

        try:
            mdx_content = generate_article(item=item, api_key=openai_api_key)
        except Exception as exc:
            console.print(f"[red]スキップ:[/red] 記事生成エラー: {exc}")
            continue

        if not mdx_content.strip():
            console.print("[yellow]スキップ:[/yellow] 空の記事が生成されました")
            continue

        # LLM がコードブロックで包んだ場合に除去する
        # 例: ```mdx\n...\n``` または ```\n...\n```
        mdx_content = mdx_content.strip()
        if mdx_content.startswith("```"):
            lines = mdx_content.split("\n")
            # 1行目のコードフェンスを除去
            lines = lines[1:]
            # 末尾のコードフェンスを除去
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            mdx_content = "\n".join(lines).strip()

        # slug を抽出してファイル名を決定
        today_str = date.today().isoformat()
        fallback_slug = f"{today_str}-article-{i}"
        slug = extract_slug(mdx_content, fallback_slug)

        # slug にファイルが既に存在する場合はスキップ
        output_path = POSTS_DIR / f"{slug}.mdx"
        if output_path.exists():
            console.print(f"[yellow]スキップ:[/yellow] {output_path.name} は既に存在します")
            continue

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(mdx_content)

        console.print(f"[green]保存完了:[/green] {output_path.name}")
        generated_count += 1

    console.print(f"\n[bold green]記事生成完了:[/bold green] {generated_count} 件保存しました")
    console.rule("[bold blue]Step 2: 記事生成完了[/bold blue]")


if __name__ == "__main__":
    main()
