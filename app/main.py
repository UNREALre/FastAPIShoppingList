# -*- coding: utf-8 -*-

from fastapi import FastAPI

from app.api import ping
from app.db import database


# Initialize the app
app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


app.include_router(ping.router)