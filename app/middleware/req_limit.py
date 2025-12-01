from app.utils.helper import get_client_ip
from app.utils.redis import get_redis_client

# 统一返回相同的show_json结构
class APIException(Exception):
    def __init__(self, code: int, msg: str, data=None):
        self.code = code
        self.msg = msg
        self.data = data


# 每日通用限流设置
async def rate_base_limit(request,prefix=str,limit=5):
    # 获取客户端IP
    ip = get_client_ip(request)
    # 设置一个KEY，包含当前日期，这样就不用每天手动去清理
    from datetime import datetime
    date_str = datetime.now().strftime("%Y%m%d")
    redis_key = prefix + f"_limit:{ip}:{date_str}"
    # 获取key的值，然后转为int判断
    redis_client = await get_redis_client()
    count = await redis_client.get(redis_key)
    # 如果存在，且大于等于limit，直接拦截
    if count and int(count) >= limit:
        return False
    
    # 否则，返回空响应，放行请求
    return True

# 指定前缀，次数安全+1
async def incr_base(request,prefix=str):
    ip = get_client_ip(request)
    from datetime import datetime, timedelta
    date_str = datetime.now().strftime("%Y%m%d")
    redis_key = prefix + f"_limit:{ip}:{date_str}"
    redis_client = await get_redis_client()
    # 使用incr命令进行自增
    count = await redis_client.incr(redis_key)
    # 如果是第一次设置，设置过期时间为24小时
    if count == 1:
        await redis_client.expire(redis_key, timedelta(hours=24))
    return None

# 针对用户ID的每日通用限流，prefix中已经包含用户ID
async def rate_user_limit(prefix=str,limit=5):
    # 设置一个KEY，包含当前日期，这样就不用每天手动去清理
    from datetime import datetime
    date_str = datetime.now().strftime("%Y%m%d")
    redis_key = prefix + f"_limit:{date_str}"
    # 获取key的值，然后转为int判断
    redis_client = await get_redis_client()
    count = await redis_client.get(redis_key)
    # 如果存在，且大于等于limit，直接拦截
    if count and int(count) >= limit:
        return False
    
    # 否则，返回空响应，放行请求
    return True

# 指定前缀，针对用户ID的次数安全+1
async def incr_user_limit(prefix=str):
    from datetime import datetime, timedelta
    date_str = datetime.now().strftime("%Y%m%d")
    redis_key = prefix + f"_limit:{date_str}"
    redis_client = await get_redis_client()
    # 使用incr命令进行自增
    count = await redis_client.incr(redis_key)
    # 如果是第一次设置，设置过期时间为24小时
    if count == 1:
        await redis_client.expire(redis_key, timedelta(hours=24))
    return None