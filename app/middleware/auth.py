from app.utils.redis import get_redis_client
from fastapi import Request, HTTPException
from app.utils.helper import show_json
from typing import Callable
from fastapi.responses import JSONResponse

# 管理员认证中间件
async def auth_admin(request: Request, call_next: Callable):
    # 获取请求路径
    path = request.url.path
    # 只对 /api/admin 开头的路径进行鉴权
    if not path.startswith("/api/admin"):
        return await call_next(request)
    # 如果是登录接口：/api/admin/login，则不需要鉴权
    if path == "/api/admin/login":
        return await call_next(request)

    # 获取请求头中的token
    auth = request.headers.get("Authorization")
    if not auth:
        return JSONResponse(status_code=401, content={"code": 401, "msg": "Token无效"})
    
    # token的格式是Bearer xxx
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JSONResponse(status_code=401, content={"code": 401, "msg": "Token无效"})
    token = parts[1]
    
    # 取出前6位作为前缀
    prefix = token[:6]
    redis = await get_redis_client()
    key = f"admin:token:{prefix}"
    # 从redis中取出对应的token
    stored_token = await redis.get(key)
    if not stored_token or stored_token != token:
        return JSONResponse(status_code=401, content={"code": 401, "msg": "Token无效"})
    
    # 鉴权通过，放行
    response = await call_next(request)
    return response

# 用户认证中间件
async def auth_user(request: Request, call_next: Callable):
    # 获取请求路径
    path = request.url.path
    # 只对 /api/user 开头的路径进行鉴权
    if not path.startswith("/api/user"):
        return await call_next(request)
    # 如果是管理员接口，则不校验用户token
    if path.startswith("/api/admin"):
        return await call_next(request)

    # 获取请求头中的token
    auth = request.headers.get("Authorization")
    if not auth:
        return JSONResponse(status_code=401, content={"code": 401, "msg": "Token无效"})
    
    # token的格式是Bearer xxx
    parts = auth.split(":")
    if len(parts) != 4:
        return JSONResponse(status_code=401, content={"code": 401, "msg": "Token无效"})
    
    redis = await get_redis_client()
    key = auth
    # 从redis中取出对应的token
    stored_token = await redis.get(key)
    if not stored_token:
        return JSONResponse(status_code=401, content={"code": 401, "msg": "Token无效"})
    
    # 鉴权通过，放行
    response = await call_next(request)
    return response