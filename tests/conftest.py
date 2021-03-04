# -*- coding: utf-8 -*-

import pytest

from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client  # testing goes within this client
