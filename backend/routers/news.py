from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import news
from ..config.database_config import get_db

# 创建APIRouter实例
# prefix 路由前缀（API接口规范文档）
# tags 分组，标签

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    categories = await news.get_categories(db,skip, limit)
    return {
        "code":200,  # 状态码
        "message":"获取新闻分类成功",
        "data":categories
    }

@router.get("/list")
async def get_news_list(
        db: AsyncSession = Depends(get_db),
        category_id: int = Query(...,alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize",le=100)
):
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db,category_id,offset,page_size)
    total = await news.get_news_count(db,category_id)
    has_more = total > offset + len(news_list)
    return{
        "code":200,
        "message":"获取新闻列表成功",
        "data":{
        "list": news_list,
        "total":total,
        "hasMore":has_more
    }
    }