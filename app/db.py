# -*- coding: utf-8 -*-

from databases import Database
from os import environ

DB_USER = environ.get('DB_USER', 'user')
DB_PASSWORD = environ.get('DB_PASS', 'password')
DB_HOST = environ.get('DB_HOST', 'localhost')
DB_NAME = environ.get('DB_NAME', 'localhost')
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'

# databases query builder
database = Database(DATABASE_URL)
