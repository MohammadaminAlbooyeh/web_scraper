"""Enhanced spider for books.toscrape.com.

This spider follows product pages to collect detailed information about each book,
including description, availability, ISBN, and more. It handles both catalog
listing pages and individual product pages.
"""

from datetime import datetime
import re
import scrapy

from books.items import ProductItem


class BookSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    # Rating mapping from text to number of stars
    RATINGS_MAP = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def parse(self, response):
        """Parse listing pages and follow links to product pages."""
        # Process each product in the listing
        for product in response.css("article.product_pod"):
            # Get the product page URL
            product_url = product.css("h3 a::attr(href)").get()
            if product_url:
                # Convert relative URL to absolute URL if necessary
                if product_url.startswith('/'):
                    product_url = response.urljoin(product_url)
                yield response.follow(
                    product_url,
                    callback=self.parse_product,
                    # Pass basic info from listing page as metadata
                    meta={
                        'listing_price': product.css(".price_color::text").get(),
                        'image_url': response.urljoin(product.css("img::attr(src)").get()),
                    }
                )

        # Follow pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        """Parse individual product pages."""
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
