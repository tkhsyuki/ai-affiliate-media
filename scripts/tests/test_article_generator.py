"""article_generator.py のユニットテスト"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from article_generator import extract_slug
from utils.llm_client import generate_article


SAMPLE_ITEM = {
    "title": "ChatGPT新機能「Projects」発表",
    "summary": "OpenAIはChatGPTの新機能「Projects」を発表しました。",
    "url": "https://example.com/chatgpt-projects",
    "published_at": "2026-08-18T10:00:00+00:00",
    "source": "newsdata",
}


# =============================================
# generate_article テスト（テストモード）
# =============================================

class TestGenerateArticle:
    def test_generate_article_mock(self):
        """テストモードでモックデータが返ってくることをテスト"""
        result = generate_article(item=SAMPLE_ITEM, api_key="test")
        assert isinstance(result, str)
        assert len(result) > 100  # 最低限の長さがある

    def test_frontmatter_keys(self):
        """生成 MDX にフロントマターの全キーが含まれることをテスト"""
        result = generate_article(item=SAMPLE_ITEM, api_key="test")
        required_keys = ["title:", "date:", "tags:", "thumbnail:", "slug:", "excerpt:", "affiliate_category:"]
        for key in required_keys:
            assert key in result, f"フロントマターに '{key}' が含まれていません"

    def test_affiliate_placeholders_amazon(self):
        """AFFILIATE_AMAZON プレースホルダーが含まれることをテスト"""
        result = generate_article(item=SAMPLE_ITEM, api_key="test")
        assert "<!-- AFFILIATE_AMAZON -->" in result, "AFFILIATE_AMAZON プレースホルダーが見つかりません"

    def test_affiliate_placeholders_a8(self):
        """AFFILIATE_A8 プレースホルダーが含まれることをテスト"""
        result = generate_article(item=SAMPLE_ITEM, api_key="test")
        assert "<!-- AFFILIATE_A8 -->" in result, "AFFILIATE_A8 プレースホルダーが見つかりません"

    def test_ai_disclosure_notice(self):
        """AI生成コンテンツの開示文が含まれることをテスト"""
        result = generate_article(item=SAMPLE_ITEM, api_key="test")
        assert "AI" in result and "作成" in result, "AI生成コンテンツの開示文が見つかりません"

    def test_has_h2_headings(self):
        """H2 見出しが含まれることをテスト"""
        result = generate_article(item=SAMPLE_ITEM, api_key="test")
        assert "## " in result, "H2 見出しが見つかりません"


# =============================================
# extract_slug テスト
# =============================================

class TestExtractSlug:
    def test_extracts_slug_from_frontmatter(self):
        """フロントマターから slug を正しく抽出できることをテスト"""
        mdx = """---
title: "テスト記事"
slug: "2026-08-18-test-article-slug"
date: "2026-08-18"
---
本文
"""
        result = extract_slug(mdx, "fallback-slug")
        assert result == "2026-08-18-test-article-slug"

    def test_slug_format(self):
        """slug が YYYY-MM-DD- で始まることをテスト"""
        result = generate_article(item=SAMPLE_ITEM, api_key="test")
        slug = extract_slug(result, "fallback")
        pattern = r"^\d{4}-\d{2}-\d{2}-"
        assert re.match(pattern, slug), f"slug '{slug}' が YYYY-MM-DD- 形式で始まっていません"

    def test_fallback_slug_when_no_match(self):
        """slug が見つからない場合はフォールバックを返すことをテスト"""
        mdx = "---\ntitle: test\n---\n本文"
        result = extract_slug(mdx, "my-fallback")
        assert result == "my-fallback"
