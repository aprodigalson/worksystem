import sqlalchemy
from worksystem.database.model.base import Base
from sqlalchemy import Column, String, Integer, Float

class Owner(Base):
    __tablename__ = 'Owner'
    # id 唯一标识符
    id = Column(Integer, primary_key=True)
    # 姓名
    name = Column(String)
    # 角色
    role = Column(String)