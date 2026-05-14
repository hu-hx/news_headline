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

@router.get("/detail")
async def get_news_detail(db:AsyncSession = Depends(get_db),news_id: int=Query(...,alias="id")):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    news_detail = await news.get_news_detail(db,news_id)
    if news_detail is None:
        raise HTTPException(status_code=404,detail="新闻不存在")

    views_judge = await news.increase_news_views(db, news_id)
    if not views_judge:
        raise HTTPException(status_code=404, detail="新闻不存在")

    related_news = await news.get_related_news(db,news_detail.id,news_detail.category_id)

    return {
        "code":200,
        "message":"success",
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publish_time":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":related_news
        }
    }


