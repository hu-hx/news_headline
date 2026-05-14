from fastapi import FastAPI
from .routers import news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 中间件 解决跨域问题

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 允许的源
    allow_credentials=True,   # 允许携带cookie
    allow_methods=["*"],      # 允许的请求方法
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(news.router)
# 接口实现流程
# 0.在config中定义数据库，仅需一次

# 1. 模块路由化（API接口规范文档 路径和相应格式）        project/routers
# 2. 定义模型类 → 数据库表（数据库格式）   project/models
# 3. 设置crud，封装数据库操作方法         project/crud
# 4. 在路由处理函数中使用crud的方法操作数据库并返回相应