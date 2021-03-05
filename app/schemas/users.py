# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, UUID4, validator


class UserCreate(BaseModel):
    """Sign up request schema."""

    email: EmailStr
    name: str
    password: str


class UserBase(BaseModel):
    """Response schema with user details."""

    id: int
    email: EmailStr
    name: str


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias='access_token')
    expires: datetime
    token_type: Optional[str] = 'bearer'

    class Config:
        allow_population_by_field_name = True

    @validator('token')
    def hexlify_token(cls, value):
        """UUID to hex string converter."""

        return value.hex


class User(UserBase):
    """Response body with user details."""
    token: TokenBase = {}
