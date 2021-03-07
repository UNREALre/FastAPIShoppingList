# -*- coding: utf-8 -*-

"""Helper functions to work with products functionality."""

from datetime import datetime

from app.db import database
from app.models.products import products_table
from app.models.users import users_table
from app.schemas import products as product_schema
from sqlalchemy import desc, func, select, and_


async def create_product(product: product_schema.Product, user):
    query = (
        products_table.insert()
        .values(
            title=product.title,
            quantity=product.quantity,
            user_id=user['id'],
        )
        .returning(
            products_table.c.id,
            products_table.c.user_id,
            products_table.c.title,
            products_table.c.quantity,
            products_table.c.created_date,
        )
    )
    product = await database.fetch_one(query)  # Here product is Record object

    product = dict(zip(product, product.values()))  # Record to dict goes here
    product['user_name'] = user['name']

    return product


async def get_product_by_id(product_id: int):
    query = (
        select(
            [
                products_table.c.id,
                products_table.c.created_date,
                products_table.c.title,
                products_table.c.quantity,
                products_table.c.user_id,
                users_table.c.name.label('user_name'),
            ]
        )
        .select_from(products_table.join(users_table))
        .where(products_table.c.id == product_id)
    )

    return await database.fetch_one(query)


async def get_products(page: int, user):
    max_per_page = 10
    current_offset = (page-1) * max_per_page
    query = (
        select(
            [
                products_table.c.id,
                products_table.c.created_date,
                products_table.c.title,
                products_table.c.quantity,
                products_table.c.user_id,
                users_table.c.name.label('user_name'),
            ]
        )
        .select_from(products_table.join(users_table))
        .where(products_table.c.user_id == user['id'])
        .order_by(desc(products_table.c.created_date))
        .limit(max_per_page)
        .offset(current_offset)
    )

    return await database.fetch_all(query)


async def get_products_num(user):
    query = (
        select(
            [
                func.count()
            ]
        )
        .select_from(products_table)
        .where(products_table.c.user_id == user['id'])
    )

    return await database.fetch_one(query)


async def update_product(product_id: int, product: product_schema.Product):
    query = (
        products_table.update()
        .where(products_table.c.id == product_id)
        .values(title=product.title, quantity=product.quantity)
    )

    return await database.fetch_one(query)
