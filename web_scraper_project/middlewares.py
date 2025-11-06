import os


class ProxyMiddleware:
    """Set a proxy on every request when SCRAPER_PROXY env var is set.

    Example: export SCRAPER_PROXY="http://user:pass@host:port"
    """

    def __init__(self):
        self.proxy = os.getenv("SCRAPER_PROXY")

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        if self.proxy:
            # Scrapy's HttpProxyMiddleware will honor request.meta['proxy']
            request.meta["proxy"] = self.proxy
