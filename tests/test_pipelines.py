"""Tests for the item processing pipelines."""

import json
import os
import sqlite3
from datetime import datetime, timezone
import pytest

from web_scraper_project.items import ProductItem
from web_scraper_project.pipelines import JsonLinesPipeline, SQLitePipeline, DATA_DIR


def _normalize_value(v):
    """Normalize values for comparison between pipeline output and input.

    This handles numbers that may be serialized as floats/Decimals and
    datetimes serialized to ISO strings by pydantic.
    """
    if v is None:
        return None
    # Numeric types (int/float) -> compare via string to avoid Decimal vs float mismatches
    try:
        # bool is subclass of int, so avoid converting booleans
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return str(v)
    except Exception:
        pass
    return str(v)


@pytest.fixture
def sample_item():
    """Create a sample ProductItem with all fields populated."""
    return ProductItem(
        title="Sample Book",
        price=9.99,
        description="A great book about testing",
        isbn="1234567890",
        upc="A123456789",
        product_type="Books",
        price_excl_tax=8.99,
        price_incl_tax=9.99,
        tax=1.00,
        availability=5,
        number_of_reviews=10,
        category="Fiction",
        star_rating=4,
        image_url="http://example.com/image.jpg",
        url="http://example.com/book",
        scrape_date="2025-11-06T10:00:00"
    )

@pytest.fixture
def tmp_data_dir(tmp_path, monkeypatch):
    """Create a temporary data directory and patch the DATA_DIR constant."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setattr("web_scraper_project.pipelines.DATA_DIR", str(data_dir))
    return data_dir


class TestJsonLinesPipeline:
    """Test suite for JsonLinesPipeline."""

    def test_process_item(self, sample_item, tmp_data_dir):
        """Test that items are correctly written to the JSON Lines file."""
        pipeline = JsonLinesPipeline()
        pipeline.open_spider(None)
        
        try:
            # Process the item
            processed_item = pipeline.process_item(sample_item, None)
            pipeline.close_spider(None)

            # Verify the file exists
            output_file = tmp_data_dir / "items.jl"
            assert output_file.exists()

            # Read and verify the contents
            with open(output_file, "r", encoding="utf-8") as f:
                saved_item = json.loads(f.readline().strip())

                # Check all fields were saved correctly (normalize types where necessary)
                fields = [
                    "title",
                    "price",
                    "description",
                    "isbn",
                    "upc",
                    "product_type",
                    "price_excl_tax",
                    "price_incl_tax",
                    "tax",
                    "availability",
                    "number_of_reviews",
                    "category",
                    "star_rating",
                    "image_url",
                    "url",
                    "scrape_date",
                ]

                for f in fields:
                    assert _normalize_value(saved_item.get(f)) == _normalize_value(sample_item.get(f))

            # Verify the item was returned unchanged
            assert processed_item == sample_item

        finally:
            # Ensure file is closed even if test fails
            if hasattr(pipeline, "file") and not pipeline.file.closed:
                pipeline.file.close()

    def test_multiple_items(self, sample_item, tmp_data_dir):
        """Test processing multiple items in sequence."""
        pipeline = JsonLinesPipeline()
        pipeline.open_spider(None)
        
        try:
            # Process multiple items
            items = [
                dict(sample_item),
                dict(sample_item, title="Another Book", price=19.99)
            ]
            
            for item in items:
                pipeline.process_item(ProductItem(item), None)
            
            pipeline.close_spider(None)

            # Verify file contents
            output_file = tmp_data_dir / "items.jl"
            with open(output_file, "r", encoding="utf-8") as f:
                saved_items = [json.loads(line.strip()) for line in f]

            assert len(saved_items) == len(items)
            assert saved_items[0]["title"] == items[0]["title"]
            assert saved_items[1]["title"] == items[1]["title"]

        finally:
            if hasattr(pipeline, "file") and not pipeline.file.closed:
                pipeline.file.close()


class TestSQLitePipeline:
    """Test suite for SQLitePipeline."""

    def test_process_item(self, sample_item, tmp_data_dir):
        """Test that items are correctly stored in SQLite database."""
        pipeline = SQLitePipeline()
        pipeline.open_spider(None)
        
        try:
            # Process the item
            processed_item = pipeline.process_item(sample_item, None)
            pipeline.close_spider(None)

            # Verify database exists
            db_path = tmp_data_dir / "items.db"
            assert db_path.exists()

            # Read and verify the contents
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check table structure
            table_info = cursor.execute("PRAGMA table_info(items)").fetchall()
            assert len(table_info) == 4  # id, item_type, data, created_at
            
            # Verify stored data
            cursor.execute("SELECT item_type, data FROM items")
            row = cursor.fetchone()
            assert row is not None
            
            item_type, data = row
            saved_item = json.loads(data)
            
            # Check item type
            assert item_type == "ProductItem"
            
            # Check all fields were saved correctly (normalize types where necessary)
            fields = [
                "title",
                "price",
                "description",
                "isbn",
                "upc",
                "product_type",
                "price_excl_tax",
                "price_incl_tax",
                "tax",
                "availability",
                "number_of_reviews",
                "category",
                "star_rating",
                "image_url",
                "url",
                "scrape_date",
            ]

            for f in fields:
                assert _normalize_value(saved_item.get(f)) == _normalize_value(sample_item.get(f))

            # Verify the item was returned unchanged
            assert processed_item == sample_item

            conn.close()

        finally:
            if hasattr(pipeline, "conn"):
                pipeline.conn.close()

    def test_multiple_items(self, sample_item, tmp_data_dir):
        """Test processing multiple items in sequence."""
        pipeline = SQLitePipeline()
        pipeline.open_spider(None)
        
        try:
            # Process multiple items
            items = [
                dict(sample_item),
                dict(sample_item, title="Another Book", price=19.99)
            ]
            
            for item in items:
                pipeline.process_item(ProductItem(item), None)
            
            pipeline.close_spider(None)

            # Verify database contents
            db_path = tmp_data_dir / "items.db"
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check number of items
            cursor.execute("SELECT COUNT(*) FROM items")
            count = cursor.fetchone()[0]
            assert count == len(items)
            
            # Check individual items
            cursor.execute("SELECT data FROM items ORDER BY id")
            saved_items = [json.loads(row[0]) for row in cursor.fetchall()]
            
            assert saved_items[0]["title"] == items[0]["title"]
            assert saved_items[1]["title"] == items[1]["title"]

            conn.close()

        finally:
            if hasattr(pipeline, "conn"):
                pipeline.conn.close()

    def test_database_schema(self, tmp_data_dir):
        """Test that the database schema is created correctly."""
        pipeline = SQLitePipeline()
        pipeline.open_spider(None)
        
        try:
            # Verify table schema
            cursor = pipeline.conn.cursor()
            table_info = cursor.execute("PRAGMA table_info(items)").fetchall()
            
            # Check column definitions
            columns = {col[1]: col[2] for col in table_info}  # name: type
            assert columns["id"] == "INTEGER"
            assert columns["item_type"] == "TEXT"
            assert columns["data"] == "TEXT"
            assert columns["created_at"] == "TEXT"
            
            # Check primary key
            pk_column = next(col for col in table_info if col[5])  # col[5] is pk flag
            assert pk_column[1] == "id"  # name of pk column

        finally:
            if hasattr(pipeline, "conn"):
                pipeline.conn.close()