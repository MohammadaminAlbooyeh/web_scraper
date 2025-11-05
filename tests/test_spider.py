import json
from scrapy.http import TextResponse, Request

from books.spiders.book_spider import BookSpider
from books.items import ProductItem


def test_book_spider_parses_listing():
    html = """
    <html>
      <body>
        <section>
          <article class="product_pod">
            <h3><a title="Test Book One">Test Book One</a></h3>
            <p class="price_color">£12.99</p>
          </article>
          <article class="product_pod">
            <h3><a title="Second Book">Second Book</a></h3>
            <p class="price_color">£7.50</p>
          </article>
          <ul class="pager">
            <li class="next"><a href="catalogue/page-2.html">next</a></li>
          </ul>
        </section>
      </body>
    </html>
    """

    url = "http://books.toscrape.com/"
    response = TextResponse(url=url, body=html.encode("utf-8"), encoding="utf-8")
    spider = BookSpider()

    results = list(spider.parse(response))

    # Extract ProductItem instances from parse output
    items = [r for r in results if isinstance(r, ProductItem)]
    assert len(items) == 2

    assert items[0]["title"] == "Test Book One"
    assert items[0]["price"] == "£12.99"

    assert items[1]["title"] == "Second Book"
    assert items[1]["price"] == "£7.50"

    # Ensure parser yields a pagination Request as well
    requests = [r for r in results if isinstance(r, Request)]
    assert len(requests) == 1
    assert "page-2.html" in requests[0].url
