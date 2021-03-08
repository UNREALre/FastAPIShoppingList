# REST API shopping-list service
This project is for the article from my blog: https://podrabinovich.ru/blog/fast-api-skeleton-project

Here I create a simple service-skeleton that can be used in other projects for fast startup. The main features of the service are:
- token-based user authorization
- user registration
- add product to personalized list
- update product
- get list of products

This service is based on FastAPI and is fully asynchronous with the help of:
- asyncpg
- databases
- uvicorn

For testing purposes I use pytest here.