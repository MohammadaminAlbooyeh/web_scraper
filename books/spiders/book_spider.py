"""A minimal spider for books.toscrape.com.

This spider yields `ProductItem` with `title`, `price` and `description` (left
empty here). It's intentionally small so you can extend it for more fields or
follow product pages for richer data.
"""

import scrapy

from books.items import ProductItem


class BookSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        """Parse listing pages and yield ProductItem instances."""
        for product in response.css("article.product_pod"):
            item = ProductItem()
            item["title"] = product.css("h3 a::attr(title)").get()
            item["price"] = product.css(".price_color::text").get()
            # description isn't available in the listing; can follow into product page
            item["description"] = None
            yield item

        # Follow pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
