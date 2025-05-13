from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

print(Config.DATABASE_URL)

db_connect = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

async def initdb():
    """creates a connection to our database"""
    
    async with db_connect.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)