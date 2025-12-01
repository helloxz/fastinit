from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import router as my_router
from .utils.redis import create_redis_pool, close_redis_pool
from fastapi.middleware.cors import CORSMiddleware
# from .model.conn import engine, Base
# 导入模型，确保后续可以被创建
# from .model import test

# 创建所有数据库表
# Base.metadata.create_all(bind=engine)

# 应用启动和关闭事件，上下文管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化Redis连接
    await create_redis_pool()
    # 启动定时任务
    # task_scheduler.start()
    yield
    # 程序关闭时关闭定时任务
    # task_scheduler.shutdown()
    await close_redis_pool()

app = FastAPI(lifespan=lifespan)


# 全局跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# 挂载路由
app.include_router(my_router)