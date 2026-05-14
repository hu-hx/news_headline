from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession


# 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=5,
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,      # 绑定数据库引擎
    class_=AsyncSession,      # 指定会话类
    expire_on_commit=False,   # 提交后会话不过期，不会重新查询数据库
)

# 依赖项，用于获取数据库对话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session           # 返回数据库会话给路由处理函数
            await session.commit()  # 提交事物
        except Exception:
            await session.rollback() # 有异常，回滚
            raise
        finally:
            await session.close()   # 关闭对话
