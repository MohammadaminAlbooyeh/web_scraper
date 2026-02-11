"""Compatibility shim: re-export items from the Scrapy project package.

This keeps `from books import ProductItem` and `from books.items import ...`
working while the authoritative implementations live in
`web_scraper_project.items`.
"""

from web_scraper_project.items import *  # noqa: F401,F403

__all__ = [
    "ProductItem",
    "ReviewItem",
    "CategoryItem",
    "SellerItem",
    "InventoryItem",
    "OrderItem",
]
    
