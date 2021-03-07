# -*- coding: utf-8 -*-

import uvicorn

from fastapi import FastAPI

from app.routers import ping, users, products
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
app.include_router(users.router)
app.include_router(products.router)


if __name__ == "__main__":  # for dev. debugging purposes
    uvicorn.run(app, host="0.0.0.0", port=8075)
