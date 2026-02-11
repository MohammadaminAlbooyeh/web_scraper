"""Scrapy project settings with sensible defaults and env overrides.

This module contains a small set of settings useful for polite scraping and
operational controls. Set environment variables to override values:
- SCRAPER_USER_AGENT
- SCRAPER_CONCURRENT_REQUESTS
- SCRAPER_DOWNLOAD_DELAY
- SCRAPER_PROXY (used by `books.middlewares.ProxyMiddleware`)
"""
import os

# Basic bot identity
BOT_NAME = os.getenv("SCRAPER_BOT_NAME", "web_scraper")
USER_AGENT = os.getenv("SCRAPER_USER_AGENT", "web_scraper (+https://example.com)")

# Tell Scrapy where to find spiders for this project. Spiders live in the
# existing `books.spiders` package (we didn't move your spider files).
SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

# Enable default item pipelines (can be adjusted in project settings)
ITEM_PIPELINES = {
    "web_scraper_project.pipelines.JsonLinesPipeline": 300,
    "web_scraper_project.pipelines.SQLitePipeline": 400,
}

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Concurrency & politeness
CONCURRENT_REQUESTS = int(os.getenv("SCRAPER_CONCURRENT_REQUESTS", "8"))
DOWNLOAD_DELAY = float(os.getenv("SCRAPER_DOWNLOAD_DELAY", "1.0"))
CONCURRENT_REQUESTS_PER_DOMAIN = int(os.getenv("SCRAPER_CONCURRENT_REQUESTS_PER_DOMAIN", "8"))

# Enable AutoThrottle for adaptive crawling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = float(os.getenv("SCRAPER_AUTOTHROTTLE_START_DELAY", "1.0"))
AUTOTHROTTLE_MAX_DELAY = float(os.getenv("SCRAPER_AUTOTHROTTLE_MAX_DELAY", "60.0"))
AUTOTHROTTLE_TARGET_CONCURRENCY = float(os.getenv("SCRAPER_AUTOTHROTTLE_TARGET_CONCURRENCY", "1.0"))

# Retries on transient errors
RETRY_ENABLED = True
RETRY_TIMES = int(os.getenv("SCRAPER_RETRY_TIMES", "3"))
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]

# Default request headers (helpful for some sites)
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Downloader middlewares: enable our lightweight ProxyMiddleware and
# ensure HttpProxyMiddleware is available.
DOWNLOADER_MIDDLEWARES = {
    "web_scraper_project.middlewares.ProxyMiddleware": 350,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": 400,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 750,
}

# Simple logging config override (can be tuned further)
LOG_LEVEL = os.getenv("SCRAPER_LOG_LEVEL", "INFO")
