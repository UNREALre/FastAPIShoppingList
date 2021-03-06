# -*- coding: utf-8 -*-

import os
import pytest

from starlette.testclient import TestClient
from sqlalchemy import create_engine

# rewriting db name before including database from db.py, to use test db in our tests
os.environ['DB_NAME'] = 'fastapi_test'

from alembic import command
from alembic.config import Config
from app import db
from app.main import app
from sqlalchemy_utils import create_database, drop_database


@pytest.fixture(scope='module')
def setup_db():
    """Fixture. Here we create DB for test purposes, yield test client for requests and finally - cleaning up."""
    try:
        create_database(db.DATABASE_URL)

        engine = create_engine(db.DATABASE_URL)
        engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

        base_dir = os.path.dirname(os.path.dirname(__file__))
        alembic_cfg = Config(os.path.join(base_dir, 'alembic.ini'))  # loading alembic config
        command.upgrade(alembic_cfg, 'head')  # perform migrations

        yield db.DATABASE_URL
    finally:
        drop_database(db.DATABASE_URL)


@pytest.fixture()
def client(setup_db):
    with TestClient(app) as test_client:
        yield test_client
