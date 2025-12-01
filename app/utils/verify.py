# 验证邮箱格式是否正确，返回BOOL
def is_valid_email(email: str) -> bool:
    import re
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))