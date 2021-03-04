# -*- coding: utf-8 -*-

import sqlalchemy

from .users import users_table

metadata = sqlalchemy.MetaData()


products_table = sqlalchemy.Table(
    'products',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey(users_table.c.id)),
    sqlalchemy.Column('title', sqlalchemy.String(100)),
    sqlalchemy.Column('quantity', sqlalchemy.Float),
    sqlalchemy.Column('created_date', sqlalchemy.DateTime, default=sqlalchemy.func.now(), nullable=False),
)
