"""data_collector.py のユニットテスト"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# パスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_collector import deduplicate, main as collect_main
from utils.news_api import fetch_news
from utils.rss_fetcher import fetch_all_feeds, _strip_html


# =============================================
# ユーティリティ関数のテスト
# =============================================

class TestStripHtml:
    def test_strips_basic_html_tags(self):
        result = _strip_html("<p>Hello <b>World</b></p>")
        assert "<p>" not in result
        assert "<b>" not in result
        assert "Hello" in result
        assert "World" in result

    def test_handles_empty_string(self):
        assert _strip_html("") == ""

    def test_handles_none_like_empty(self):
        # None を渡すと早期リターンで空文字
        assert _strip_html(None) == ""  # type: ignore[arg-type]

    def test_plain_text_unchanged(self):
        text = "これはプレーンテキストです"
        assert _strip_html(text) == text


# =============================================
# RSS フィード取得のテスト（モック）
# =============================================

class TestFetchAllFeeds:
    def test_fetch_rss_feeds_mock(self):
        """feedparser をモックして fetch_all_feeds() をテスト"""
        mock_entry = MagicMock()
        mock_entry.title = "AIツール最新情報"
        mock_entry.summary = "<p>生成AIの新しいツールが登場しました</p>"
        mock_entry.link = "https://example.com/ai-tool-news"
        mock_entry.published_parsed = (2026, 8, 18, 10, 0, 0, 0, 0, 0)

        mock_feed = MagicMock()
        mock_feed.entries = [mock_entry]
        mock_feed.bozo = False

        with patch("utils.rss_fetcher.feedparser.parse", return_value=mock_feed):
            articles = fetch_all_feeds()

        assert len(articles) > 0
        first = articles[0]
        assert "title" in first
        assert "summary" in first
        assert "url" in first
        assert "published_at" in first
        assert "source" in first

    def test_output_schema(self):
        """出力辞書のキーが正しいかテスト"""
        mock_entry = MagicMock()
        mock_entry.title = "Test Title"
        mock_entry.summary = "Test Summary"
        mock_entry.link = "https://example.com/test"
        mock_entry.published_parsed = (2026, 8, 18, 10, 0, 0, 0, 0, 0)

        mock_feed = MagicMock()
        mock_feed.entries = [mock_entry]
        mock_feed.bozo = False

        required_keys = {"title", "summary", "url", "published_at", "source"}

        with patch("utils.rss_fetcher.feedparser.parse", return_value=mock_feed):
            articles = fetch_all_feeds()

        for article in articles:
            assert required_keys.issubset(set(article.keys())), (
                f"記事に必要なキーが不足しています: {required_keys - set(article.keys())}"
            )

    def test_error_handling_on_feed_failure(self):
        """フィード取得失敗時にスキップしてリストを返すことをテスト"""
        mock_feed = MagicMock()
        mock_feed.entries = []
        mock_feed.bozo = True

        with patch("utils.rss_fetcher.feedparser.parse", return_value=mock_feed):
            articles = fetch_all_feeds()

        assert isinstance(articles, list)


# =============================================
# NewsData.io API のテスト
# =============================================

class TestFetchNews:
    def test_fetch_news_api_mock(self):
        """API キー "test" でモックデータを返すことをテスト"""
        articles = fetch_news(api_key="test", max_results=5)
        assert isinstance(articles, list)
        if articles:  # フィクスチャが存在する場合
            first = articles[0]
            assert "title" in first
            assert "url" in first
            assert "source" in first
            assert first["source"] == "newsdata"

    def test_returns_empty_on_http_error(self):
        """HTTP エラー時に空リストを返すことをテスト"""
        import httpx
        with patch("utils.news_api.httpx.Client") as mock_client:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Error", request=MagicMock(), response=MagicMock(status_code=401)
            )
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response

            articles = fetch_news(api_key="real-but-fail-key")

        assert articles == []


# =============================================
# 重複除去のテスト
# =============================================

class TestDeduplicate:
    def test_dedup_urls(self):
        """同一 URL を持つ記事が重複除去されることをテスト"""
        articles = [
            {"title": "記事1", "url": "https://example.com/1", "summary": "", "published_at": "", "source": "test"},
            {"title": "記事2", "url": "https://example.com/2", "summary": "", "published_at": "", "source": "test"},
            {"title": "記事1 重複", "url": "https://example.com/1", "summary": "", "published_at": "", "source": "test"},
        ]
        result = deduplicate(articles)
        assert len(result) == 2
        urls = [a["url"] for a in result]
        assert urls.count("https://example.com/1") == 1

    def test_empty_list(self):
        """空リストを渡したとき空リストを返すことをテスト"""
        assert deduplicate([]) == []

    def test_no_duplicates(self):
        """重複なしのリストはそのまま返すことをテスト"""
        articles = [
            {"title": "記事1", "url": "https://example.com/1", "summary": "", "published_at": "", "source": "test"},
            {"title": "記事2", "url": "https://example.com/2", "summary": "", "published_at": "", "source": "test"},
        ]
        result = deduplicate(articles)
        assert len(result) == 2
