import sqlalchemy.ext.asyncio as _asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config.config import settings
from sqlalchemy import text

DATABASE_URL = settings.DB_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def execute_raw_sql(query: str, *params):
    async with engine.connect() as conn:
        result = await conn.execute(text(query), params)
        await conn.commit()
        return result 
