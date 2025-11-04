import json
import sqlite3
import os

import pytest

import books.pipelines as pipelines


def test_jsonlines_pipeline_writes_file(tmp_path, monkeypatch):
    # Redirect DATA_DIR to a temporary directory
    monkeypatch.setattr(pipelines, "DATA_DIR", str(tmp_path))

    pipe = pipelines.JsonLinesPipeline()
    pipe.open_spider(spider=None)

    item = {"title": "Test Book", "price": "£9.99"}
    pipe.process_item(item, spider=None)
    pipe.close_spider(spider=None)

    jl_path = os.path.join(str(tmp_path), "items.jl")
    assert os.path.exists(jl_path)

    with open(jl_path, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    assert len(lines) == 1

    parsed = json.loads(lines[0])
    assert parsed == item


def test_sqlite_pipeline_inserts_item(tmp_path, monkeypatch):
    # Redirect DATA_DIR to a temporary directory
    monkeypatch.setattr(pipelines, "DATA_DIR", str(tmp_path))

    pipe = pipelines.SQLitePipeline()
    pipe.open_spider(spider=None)

    item = {"title": "SQLite Book", "price": "£5.00"}
    pipe.process_item(item, spider=None)
    pipe.close_spider(spider=None)

    db_path = os.path.join(str(tmp_path), "items.db")
    assert os.path.exists(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, item_type, data, created_at FROM items")
    rows = cur.fetchall()
    conn.close()

    assert len(rows) == 1
    _id, item_type, data_json, created_at = rows[0]
    assert item_type == "dict"
    data = json.loads(data_json)
    assert data == item
    assert isinstance(created_at, str) and len(created_at) > 0