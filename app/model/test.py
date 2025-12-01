from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .conn import Base

class TestModel(Base):
    # 表名称
    __tablename__ = "test_table"
    # 备注信息
    __table_args__ = {"comment": "测试表"}

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    name = Column(String(100), nullable=False, comment="名称")
    description = Column(Text, nullable=True, comment="描述信息")

    # 声明函数
    @classmethod
    def get_by_id(cls, db_session, record_id: int):
        """根据ID获取记录"""
        return db_session.query(cls).filter(cls.id == record_id).first()