# -*- coding: utf-8 -*-

import asyncio
import pytest

from fastapi.testclient import TestClient

from app.utils.users import create_user_token


def get_user_token(client: TestClient, user_data):
    response = client.post('/auth', data=user_data)
    token = response.json()['access_token']

    return token


def test_create_product(client: TestClient):
    request_data = {
        'email': 'neo@matrix.com',
        'name': 'Mr. Anderson',
        'password': 'red_pill',
    }
    client.post('/sign-up', json=request_data)

    user_data = {
        'username': 'neo@matrix.com',
        'password': 'red_pill',
    }
    token = get_user_token(client, user_data)

    request_data = {
        'title': 'Bananas',
        'quantity': 3,
    }
    response = client.post('/products', json=request_data, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 201
    assert response.json()['title'] == 'Bananas'
    assert response.json()['quantity'] == 3
    assert response.json()['user_name'] == 'Mr. Anderson'


def test_get_products(client: TestClient):
    user_data = {
        'username': 'neo@matrix.com',
        'password': 'red_pill',
    }
    token = get_user_token(client, user_data)

    response = client.get('/products', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json()['total']['count_1'] == 1
    assert response.json()['results'][0]['id'] == 1
    assert response.json()['results'][0]['title'] == 'Bananas'


def test_get_product(client: TestClient):
    user_data = {
        'username': 'neo@matrix.com',
        'password': 'red_pill',
    }
    token = get_user_token(client, user_data)

    response = client.get('/products/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['title'] == 'Bananas'
    assert response.json()['quantity'] == 3


def test_get_not_existed_product(client: TestClient):
    user_data = {
        'username': 'neo@matrix.com',
        'password': 'red_pill',
    }
    token = get_user_token(client, user_data)

    response = client.get('/products/2', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


def test_get_not_owned_product(client: TestClient):
    request_data = {
        'email': 'smith@matrix.com',
        'name': 'Agent Smith',
        'password': 'virus',
    }
    client.post('/sign-up', json=request_data)

    user_data = {
        'username': 'smith@matrix.com',
        'password': 'virus',
    }
    token = get_user_token(client, user_data)

    response = client.get('/products/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


def test_update_product(client: TestClient):
    user_data = {
        'username': 'neo@matrix.com',
        'password': 'red_pill',
    }
    token = get_user_token(client, user_data)

    request_data = {
        'title': 'Milk',
        'quantity': 1,
    }
    response = client.put('/products/1', headers={'Authorization': f'Bearer {token}'}, json=request_data)

    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['title'] == 'Milk'
    assert response.json()['quantity'] == 1


def test_update_not_owned_product(client: TestClient):
    user_data = {
        'username': 'smith@matrix.com',
        'password': 'virus',
    }
    token = get_user_token(client, user_data)

    request_data = {
        'title': 'Milk',
        'quantity': 1,
    }
    response = client.put('/products/1', headers={'Authorization': f'Bearer {token}'}, json=request_data)

    assert response.status_code == 403
