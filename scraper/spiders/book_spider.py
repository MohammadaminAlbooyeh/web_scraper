"""Enhanced spider for books.toscrape.com.

This spider follows product pages to collect detailed information about each book,
including description, availability, ISBN, and more. It handles both catalog
listing pages and individual product pages.
"""

import asyncio
import aiohttp
from aiohttp import ClientSession

from books.items import ProductItem


class AsyncBookSpider:
    def __init__(self):
        self.start_urls = ["http://books.toscrape.com/"]

    async def fetch(self, url, session):
        async with session.get(url) as response:
            return await response.text()

    async def parse_listing(self, html, session):
        """Parse the listing page and extract product URLs."""
        # Example: Use BeautifulSoup or another parser to extract links
        pass

    async def parse_product(self, html):
        """Parse the product page and extract details."""
        item = ProductItem()

        # Basic Information
        item['title'] = response.css(".product_main h1::text").get()
        item['price'] = response.meta.get('listing_price')
        item['description'] = response.css("#product_description + p::text").get()
        item['url'] = response.url
        item['image_url'] = response.meta.get('image_url')
        item['scrape_date'] = datetime.utcnow().isoformat()

        # Extract product information from table
        rows = response.css("table tr")
        info_map = {
            'UPC': 'upc',
            'Product Type': 'product_type',
            'Price (excl. tax)': 'price_excl_tax',
            'Price (incl. tax)': 'price_incl_tax',
            'Tax': 'tax',
            'Availability': 'availability',
            'Number of reviews': 'number_of_reviews'
        }
        
        for row in rows:
            header = row.css("th::text").get()
            if header in info_map:
                item[info_map[header]] = row.css("td::text").get()

        # Categories
        breadcrumbs = response.css(".breadcrumb li:not(:first-child) a::text").getall()
        item['category'] = breadcrumbs[-1] if breadcrumbs else None

        # Star Rating
        star_class = response.css(".star-rating::attr(class)").get()
        if star_class:
            rating_text = star_class.split()[-1]
            item['star_rating'] = self.RATINGS_MAP.get(rating_text)

        # Clean up availability to extract number
        if item.get('availability'):
            stock_text = item['availability']
            stock_match = re.search(r'\d+', stock_text)
            if stock_match:
                item['availability'] = int(stock_match.group())

        # Clean up prices to remove currency symbols and convert to float
        for price_field in ['price', 'price_excl_tax', 'price_incl_tax', 'tax']:
            if item.get(price_field):
                price_str = item[price_field]
                price_match = re.search(r'[\d.]+', price_str)
                if price_match:
                    item[price_field] = float(price_match.group())

        yield item

    async def scrape(self):
        async with ClientSession() as session:
            tasks = []
            for url in self.start_urls:
                tasks.append(self.fetch(url, session))
            responses = await asyncio.gather(*tasks)
            for html in responses:
                await self.parse_listing(html, session)

if __name__ == "__main__":
    spider = AsyncBookSpider()
    asyncio.run(spider.scrape())
