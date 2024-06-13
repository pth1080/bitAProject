from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from app.serializers.base import PaginateRequest


class OrderByFilter(Enum):
    CREATED_AT = 'created_at'
    NAME = 'name'
    CURRENT_PRICE = 'current_price'
    RATE = 'rate'


class GetProductRequest(PaginateRequest):
    search: Optional[str] = None
    order_by: OrderByFilter = Field(OrderByFilter.CREATED_AT)
    desc: bool = Field(default=True)


class ProductImageSerializer(BaseModel, from_attributes=True):
    url: str
    is_main: bool


class ProductInfoSerializer(BaseModel, from_attributes=True):
    name: str
    current_price: int
    original_price: int
    # optional fields
    discount_percent: Optional[int] = 0
    rate: Optional[int] = 0
    rate_counts: Optional[int] = 0
    sold: Optional[int] = 0
    location: Optional[str] = ''
    product_images: Optional[List[ProductImageSerializer]] = []
