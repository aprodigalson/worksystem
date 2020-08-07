import sqlalchemy
from worksystem.database.model.base import Base
from sqlalchemy import Column, String, Integer, Float, Enum

class Owner(Base):
    __tablename__ = 'Owner'
    # id 唯一标识符
    id = Column(Integer, primary_key=True)
    # 姓名
    name = Column(String)
    # 角色
    role = Column(Enum('业主','工作人员'))

    def __repr__(self):
        return 'id: %s, name: %s, role:%s \n'% (self.id, self.name, self.role)