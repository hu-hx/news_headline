from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.news import Category, News


async def get_categories(db:AsyncSession,skip: int = 0, limit: int = 100):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()

async def get_news_list(db:AsyncSession,category_id:int,skip: int = 0, limit: int = 10):
    result = await db.execute(select(News).offset(skip).limit(limit).where(News.category_id == category_id))
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int):
    # 查询指定分类下的新闻数量
    result = await db.execute(select(func.count(News.id)).where(News.category_id == category_id))
    return result.scalars().one()