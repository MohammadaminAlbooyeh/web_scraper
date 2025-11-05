import os
import json
import sqlite3
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    return DATA_DIR


# Try to import pydantic schemas for optional validation. Validation is
# performed only when an appropriate schema exists for the incoming item
# type (e.g. ProductItem -> ProductModel). If pydantic is not installed the
# pipelines will continue to work without validation.
try:
    from .schemas import (
        ProductModel,
        ReviewModel,
        CategoryModel,
        SellerModel,
        InventoryModel,
        OrderModel,
    )

    SCHEMA_MAP = {
        "ProductItem": ProductModel,
        "ReviewItem": ReviewModel,
        "CategoryItem": CategoryModel,
        "SellerItem": SellerModel,
        "InventoryItem": InventoryModel,
        "OrderItem": OrderModel,
    }
except Exception:
    SCHEMA_MAP = {}


class JsonLinesPipeline:
    """
    Writes each item as one JSON object per line into data/items.jl
    """

    def open_spider(self, spider):
        _ensure_data_dir()
        self.filepath = os.path.join(DATA_DIR, "items.jl")
        self.file = open(self.filepath, "w", encoding="utf-8")

    def close_spider(self, spider):
        if hasattr(self, "file") and not self.file.closed:
            self.file.close()

    def process_item(self, item, spider):
        # Attempt to validate/serialize using pydantic schema when available.
        item_dict = dict(item)
        item_type = getattr(item, "__class__", None)
        item_type_name = item_type.__name__ if item_type else type(item).__name__

        schema = SCHEMA_MAP.get(item_type_name)
        if schema is not None:
            # Validate and produce JSON using pydantic
            obj = schema.parse_obj(item_dict)
            line = obj.json(ensure_ascii=False)
        else:
            line = json.dumps(item_dict, ensure_ascii=False)

        self.file.write(line + "\n")
        return item


class SQLitePipeline:
    """
    Stores items in a simple SQLite table (id, item_type, data, created_at).
    The data column contains the full item as a JSON string.
    """

    def open_spider(self, spider):
        _ensure_data_dir()
        self.db_path = os.path.join(DATA_DIR, "items.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_type TEXT,
                data TEXT,
                created_at TEXT
            )
            """
        )
        self.conn.commit()

    def close_spider(self, spider):
        if hasattr(self, "conn"):
            self.conn.commit()
            self.conn.close()

    def process_item(self, item, spider):
        item_type = getattr(item, "__class__", None)
        item_type_name = item_type.__name__ if item_type else type(item).__name__

        item_dict = dict(item)
        schema = SCHEMA_MAP.get(item_type_name)
        if schema is not None:
            obj = schema.parse_obj(item_dict)
            data_json = obj.json(ensure_ascii=False)
        else:
            data_json = json.dumps(item_dict, ensure_ascii=False)

        created_at = datetime.utcnow().isoformat() + "Z"
        self.conn.execute(
            "INSERT INTO items (item_type, data, created_at) VALUES (?, ?, ?)",
            (item_type_name, data_json, created_at),
        )
        # commit periodically to avoid long transactions; keep simple here
        self.conn.commit()
        return item
