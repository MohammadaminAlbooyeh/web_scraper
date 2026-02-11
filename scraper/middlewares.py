"""Compatibility shim: re-export middlewares from the Scrapy project package.

The authoritative implementations live in `web_scraper_project.middlewares`.
Keeping a shim at `books.middlewares` preserves backwards compatibility for
imports elsewhere in the repository.
"""

from web_scraper_project.middlewares import *  # noqa: F401,F403

__all__ = ["ProxyMiddleware"]
