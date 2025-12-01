from app.config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

DB_USER = config.get("db.user")
DB_PASSWORD = config.get("db.password")
DB_HOST = config.get("db.host", "localhost")
DB_PORT = config.get("db.port", 5432)
DB_NAME = config.get("db.database")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 推荐的数据库会话管理器
@contextmanager
def get_db():
    """数据库会话上下文管理器，自动提交/回滚和关闭连接"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

'''后续使用示例，with是上下文管理器，确保正确关闭连接
with get_db() as db:
        return db.query(User).filter(User.id == user_id).first()
'''