# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    """Validate request data."""

    title: str
    quantity: float


class ProductDetails(Product):
    """Response schema."""

    id: int
    user_id: int
    user_name: str
    created_date: datetime
