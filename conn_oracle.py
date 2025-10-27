import config
import oracledb
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Database connection details (consider using environment variables for security)
DB_USER = config.db_conn_info.userid
DB_PASSWORD = config.db_conn_info.password
DB_CONNECT_STRING = f"{config.db_conn_info.host}:{config.db_conn_info.port}/{config.db_conn_info.database}"

# Connection pool (optional, but recommended for performance)
pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = oracledb.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_CONNECT_STRING,
        min=2, # Minimum number of connections in the pool
        max=5, # Maximum number of connections in the pool
        increment=1, # How many connections to create when the pool needs to grow
        encoding="UTF-8"
    )
    yield
    pool.release() # Release the pool when the application shuts down

async def get_db_connection():
    connection = None
    try:
        connection = pool.acquire() # Acquire connection from the pool
        yield connection
    finally:
        if connection:
            pool.release(connection) # Release connection back to the pool
