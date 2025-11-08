"""Offline integration test: feed saved HTML fixtures to the spider and pipelines.

This test uses local HTML fixtures so it can run without network access. It
exercises the spider's listing -> product flow and verifies that pipelines
accept and persist the validated items.
"""

import json
import os
from pathlib import Path
from scrapy.http import TextResponse, Request

import pytest

from books.spiders.book_spider import BookSpider
from web_scraper_project.items import ProductItem
from web_scraper_project import pipelines


def _load_fixture(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def make_response(url: str, body: str) -> TextResponse:
    return TextResponse(url=url, body=body.encode("utf-8"), encoding="utf-8")


def test_spider_parse_listing_then_product(tmp_path, monkeypatch):
    # Prepare fixtures
    base = Path(__file__).parent.parent / "fixtures"
    listing_html = _load_fixture(base / "listing.html")
    product_html = _load_fixture(base / "product.html")

    spider = BookSpider()

    # Simulate listing page response
    listing_resp = make_response("http://books.toscrape.com/", listing_html)
    parse_results = list(spider.parse(listing_resp))

    # Expect at least one Request to product page
    requests = [r for r in parse_results if isinstance(r, Request)]
    assert requests, "Spider.parse should yield Requests to product pages"

    # Patch pipeline DATA_DIR to tmp_path/data
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setattr(pipelines, "DATA_DIR", str(data_dir))

    # Initialize pipelines
    json_pipe = pipelines.JsonLinesPipeline()
    sqlite_pipe = pipelines.SQLitePipeline()
    json_pipe.open_spider(spider)
    sqlite_pipe.open_spider(spider)

    try:
        # For each product request, simulate the product page response
        for req in requests:
            # Create product response at the absolute URL used by the spider
            product_resp = make_response("http://books.toscrape.com/catalogue/sample-book_1/index.html", product_html)
            # Call the spider's callback (parse_product)
            results = list(spider.parse_product(product_resp))
            # There should be at least one item
            items = [it for it in results if isinstance(it, ProductItem)]
            assert items, "parse_product should yield a ProductItem"

            # Process item through pipelines
            for item in items:
                json_pipe.process_item(item, spider)
                sqlite_pipe.process_item(item, spider)

        # Close pipelines
        json_pipe.close_spider(spider)
        sqlite_pipe.close_spider(spider)

        # Check JSON lines file
        jl = data_dir / "items.jl"
        assert jl.exists()
        with jl.open("r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f]
        assert lines, "items.jl should contain at least one saved item"

        # Check sqlite DB
        db = data_dir / "items.db"
        assert db.exists(), "SQLite DB should exist"

    finally:
        # Ensure tidy close if something fails
        try:
            json_pipe.close_spider(spider)
        except Exception:
            pass
        try:
            sqlite_pipe.close_spider(spider)
        except Exception:
            pass
