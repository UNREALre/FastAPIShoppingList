# -*- coding: utf-8 -*-

import asyncio
import pytest

from fastapi.testclient import TestClient

from app.schemas.users import UserCreate
from app.utils.users import create_user_token, create_user


def test_sign_up(client: TestClient):  # temp_db fixture from conftest module
    request_data = {
        'email': 'neo@matrix.com',
        'name': 'Mr. Anderson',
        'password': 'red_pill',
    }

    response = client.post('/sign-up', json=request_data)
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['email'] == 'neo@matrix.com'
    assert response.json()['name'] == 'Mr. Anderson'
    assert response.json()['token']['expires'] is not None
    assert response.json()['token']['access_token'] is not None


def test_login(client: TestClient):
    request_data = {
        'username': 'neo@matrix.com',
        'password': 'red_pill',
    }

    response = client.post('/auth', data=request_data)
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
    assert response.json()['expires'] is not None
    assert response.json()['access_token'] is not None


def test_invalid_login(client: TestClient):
    request_data = {
        'username': 'neo@matrix.com',
        'password': 'blue_pill',
    }

    response = client.post('/auth', data=request_data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Wrong e-mail or password'


def test_user_detail(client: TestClient):
    loop = asyncio.get_event_loop()
    token = loop.run_until_complete(create_user_token(user_id=1))
    response = client.get('/users/me', headers={'Authorization': f'Bearer {token["token"]}'})
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['email'] == 'neo@matrix.com'
    assert response.json()['name'] == 'Mr. Anderson'


def test_user_detail_forbidden_without_token(client: TestClient):
    response = client.get('/users/me')
    assert response.status_code == 401


@pytest.mark.freeze_time('2010-01-01')
def test_user_detail_forbidden_with_expired_token(client: TestClient, freezer):
    user = UserCreate(
        email='smith@agent.net',
        name='Mr. Smith',
        password='virus',
    )
    loop = asyncio.get_event_loop()
    user_db = loop.run_until_complete(create_user(user))
    freezer.move_to("'2010-02-01'")
    response = client.get('/users/me', headers={'Authorization': f'Bearer {user_db["token"]["token"]}'})
    assert response.status_code == 401
