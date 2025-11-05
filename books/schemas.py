from typing import Optional
from pydantic import BaseModel


class ProductModel(BaseModel):
    title: Optional[str]
    price: Optional[str]
    description: Optional[str] = None


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
