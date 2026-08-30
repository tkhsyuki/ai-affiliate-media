"""パイプライン エントリポイント — Step 1 + Step 2 を順番に実行する"""
from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console

sys.path.insert(0, str(Path(__file__).parent))

from data_collector import main as collect
from article_generator import main as generate

console = Console()


def main() -> None:
    console.rule("[bold magenta]AI Tools Journal -- 自動パイプライン開始[/bold magenta]")

    # Step 1: データ収集
    articles = collect()

    # Step 2: 記事生成
    generate(articles=articles)

    console.rule("[bold magenta]パイプライン完了[/bold magenta]")


if __name__ == "__main__":
    main()
