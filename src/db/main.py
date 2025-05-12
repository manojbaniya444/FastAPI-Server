from sqlmodel import create_engine, text
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
        statement = text("select 'Hi Data'")
        result = await conn.execute(statement)
        print(result)