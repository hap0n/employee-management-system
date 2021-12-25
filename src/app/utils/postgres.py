from contextlib import asynccontextmanager
from os import getenv

import asyncpg

_connection_pool: asyncpg.pool.Pool = None


async def connection_pool() -> asyncpg.pool.Pool:
    global _connection_pool

    if not _connection_pool:
        _connection_pool = await asyncpg.create_pool(
            user=getenv("EMS_DB_USER"),
            password=getenv("EMS_DB_PASS"),
            host=getenv("EMS_DB_HOST"),
            port=getenv("EMS_DB_PORT"),
            database=getenv("EMS_DB_NAME"),
            max_size=int(getenv("ANN_TOOL_DB_CONNECTION_POOL_SIZE", 10)),
        )

    return _connection_pool


@asynccontextmanager
async def db_connection():
    pool = await connection_pool()
    async with pool.acquire() as conn:
        yield conn
