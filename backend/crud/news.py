from sqlalchemy import select, func, update
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

async def get_news_detail(db:AsyncSession,news_id:int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db:AsyncSession,news_id:int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 → 检查数据库是否真的命中了数据 → 命中返回True
    return result.rowcount > 0

async def get_related_news(db:AsyncSession,news_id:int, category_id:int,limit: int = 5):
    stmt = (select(News).where(News.id != news_id, News.category_id == category_id).
            order_by(News.views.desc(),News.publish_time.desc()).limit(limit))
    result = await db.execute(stmt)
    return result.scalars().all()