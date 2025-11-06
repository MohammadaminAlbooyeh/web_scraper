from typing import Optional
from pydantic import BaseModel


"""Schema definitions for data validation using Pydantic.

This module defines the data models and validation rules for items scraped from
books.toscrape.com. It uses Pydantic for runtime type checking and data validation,
ensuring that all scraped data meets our quality standards before storage.
"""

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, HttpUrl, validator, Field


class ProductModel(BaseModel):
    """Validates and normalizes book product data.
    
    This model enforces the following validation rules:
    1. Basic Information:
       - title: Required, non-empty string
       - price: Non-negative decimal number
       - description: Optional text
       
    2. Book Details:
       - isbn: Optional, must be 10 or 13 digits when provided
       - upc: Required, non-empty string
       - product_type: Required string
       
    3. Pricing:
       - price_excl_tax: Non-negative decimal
       - price_incl_tax: Non-negative decimal, must equal price_excl_tax + tax
       - tax: Non-negative decimal
       
    4. Inventory:
       - availability: Non-negative integer
       - number_of_reviews: Non-negative integer
       
    5. Categories and Rating:
       - category: Optional string
       - star_rating: Integer between 1 and 5
       
    6. URLs:
       - image_url: Valid HTTP/HTTPS URL
       - url: Valid HTTP/HTTPS URL
       
    7. Meta:
       - scrape_date: Datetime, cannot be in the future
    
    Examples:
        >>> data = {
        ...     "title": "Sample Book",
        ...     "price": "9.99",
        ...     "isbn": "1234567890",
        ...     "upc": "ABC123",
        ...     "product_type": "Books",
        ...     "price_excl_tax": "8.99",
        ...     "price_incl_tax": "9.99",
        ...     "tax": "1.00",
        ...     "availability": 5,
        ...     "number_of_reviews": 10,
        ...     "star_rating": 4,
        ...     "image_url": "https://example.com/image.jpg",
        ...     "url": "https://example.com/book",
        ...     "scrape_date": "2025-11-06T10:00:00"
        ... }
        >>> product = ProductModel(**data)
    """
    
    # Basic Information
    title: str = Field(
        ...,
        description="The book title, required and non-empty"
    )
    price: Decimal = Field(
        ...,
        ge=0,
        description="The current price of the book (must be non-negative)"
    )
    description: Optional[str] = Field(
        None,
        description="Optional book description or summary"
    )
    
    # Book Specific Details
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    upc: str = Field(..., min_length=1)
    product_type: str
    price_excl_tax: Decimal = Field(..., ge=0)
    price_incl_tax: Decimal = Field(..., ge=0)
    tax: Decimal = Field(..., ge=0)
    availability: int = Field(..., ge=0)
    number_of_reviews: int = Field(..., ge=0)
    
    # Categories and Rating
    category: Optional[str] = None
    star_rating: int = Field(..., ge=1, le=5)
    
    # Product Images and URLs
    image_url: HttpUrl
    url: HttpUrl
    
    # Meta Information
    scrape_date: datetime

    @validator('isbn')
    def validate_isbn(cls, v):
        if v is not None:
            # Remove hyphens and spaces
            v = v.replace('-', '').replace(' ', '')
            if not v.isdigit():
                raise ValueError('ISBN must contain only digits')
            if len(v) not in (10, 13):
                raise ValueError('ISBN must be 10 or 13 digits')
        return v

    @validator('price_incl_tax')
    def validate_price_incl_tax(cls, v, values):
        if 'price_excl_tax' in values and 'tax' in values:
            expected = values['price_excl_tax'] + values['tax']
            if abs(v - expected) > Decimal('0.01'):  # Allow for small rounding differences
                raise ValueError('price_incl_tax must equal price_excl_tax + tax')
        return v

    @validator('scrape_date')
    def validate_scrape_date(cls, v):
        if v > datetime.now():
            raise ValueError('scrape_date cannot be in the future')
        return v


class ReviewModel(BaseModel):
    product_id: Optional[str]
    reviewer_name: Optional[str]
    rating: Optional[str]
    comment: Optional[str]


class CategoryModel(BaseModel):
    name: Optional[str]
    url: Optional[str]


class SellerModel(BaseModel):
    name: Optional[str]
    rating: Optional[str]
    location: Optional[str]


class InventoryModel(BaseModel):
    product_id: Optional[str]
    stock_quantity: Optional[int]
    warehouse_location: Optional[str]


class OrderModel(BaseModel):
    order_id: Optional[str]
    product_id: Optional[str]
    quantity: Optional[int]
    order_date: Optional[str]
    customer_name: Optional[str]
