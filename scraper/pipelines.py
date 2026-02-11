"""Compatibility shim: re-export pipelines from the Scrapy project package.

The authoritative pipeline implementations live in
`web_scraper_project.pipelines`. Keeping a shim at `books.pipelines` keeps
backwards compatibility for imports in tests and other modules.
"""

from web_scraper_project.pipelines import *  # noqa: F401,F403

__all__ = ["JsonLinesPipeline", "SQLitePipeline"]
