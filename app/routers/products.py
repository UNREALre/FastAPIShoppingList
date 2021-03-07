# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.products import Product, ProductDetails
from app.schemas.users import User
from app.utils import products as product_utils
from app.utils.dependecies import get_current_user

router = APIRouter()


@router.post('/products', response_model=ProductDetails, status_code=201)
async def create_product(product: Product, current_user: User = Depends(get_current_user)):
    product = await product_utils.create_product(product, current_user)
    return product


@router.get('/products')
async def get_products(page: int = 1, current_user: User = Depends(get_current_user)):
    products_num = await product_utils.get_products_num(current_user)
    products = await product_utils.get_products(page, current_user)
    return {'total': products_num, 'results': products}


@router.get('/products/{product_id}', response_model=ProductDetails)
async def get_product(product_id: int, current_user: User = Depends(get_current_user)):
    product = await product_utils.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if product['user_id'] != current_user['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You don\'t have access',
        )

    return product


@router.put('/products/{product_id}', response_model=ProductDetails)
async def update_product(product_id: int, product_data: Product, current_user: User = Depends(get_current_user)):
    product = await product_utils.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if product['user_id'] != current_user['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You don\'t have access',
        )

    await product_utils.update_product(product_id, product_data)

    return await product_utils.get_product_by_id(product_id)
