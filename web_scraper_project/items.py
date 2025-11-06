import scrapy


class ProductItem(scrapy.Item):
    # Basic Information
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    
    # Book Specific Details
    isbn = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
    
    # Categories and Rating
    category = scrapy.Field()
    star_rating = scrapy.Field()
    
    # Product Images
    image_url = scrapy.Field()
    
    # Meta Information
    url = scrapy.Field()
    scrape_date = scrapy.Field()


class ReviewItem(scrapy.Item):
    product_id = scrapy.Field()
    reviewer_name = scrapy.Field()
    rating = scrapy.Field()
    comment = scrapy.Field()


class CategoryItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class SellerItem(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    location = scrapy.Field()


class InventoryItem(scrapy.Item):
    product_id = scrapy.Field()
    stock_quantity = scrapy.Field()
    warehouse_location = scrapy.Field()


class OrderItem(scrapy.Item):
    order_id = scrapy.Field()
    product_id = scrapy.Field()
    quantity = scrapy.Field()
    order_date = scrapy.Field()
    customer_name = scrapy.Field()
