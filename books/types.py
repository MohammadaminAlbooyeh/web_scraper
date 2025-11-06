from typing import TypedDict, Optional


class ProductDict(TypedDict, total=False):
    title: Optional[str]
    price: Optional[str]
    description: Optional[str]


class ReviewDict(TypedDict, total=False):
    product_id: Optional[str]
    reviewer_name: Optional[str]
    rating: Optional[str]
    comment: Optional[str]


class CategoryDict(TypedDict, total=False):
    name: Optional[str]
    url: Optional[str]


class SellerDict(TypedDict, total=False):
    name: Optional[str]
    rating: Optional[str]
    location: Optional[str]


class InventoryDict(TypedDict, total=False):
    product_id: Optional[str]
    stock_quantity: Optional[int]
    warehouse_location: Optional[str]


class OrderDict(TypedDict, total=False):
    order_id: Optional[str]
    product_id: Optional[str]
    quantity: Optional[int]
    order_date: Optional[str]
    customer_name: Optional[str]
