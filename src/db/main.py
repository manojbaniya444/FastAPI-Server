from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

print(Config.DATABASE_URL)

db_connect = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

async def initdb():
    """creates a connection to our database"""
    
    async with db_connect.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
async def get_session():
    """
    Dependency to provide the session object
    """
    async_session = sessionmaker(
        bind=db_connect, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session