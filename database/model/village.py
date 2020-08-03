import sqlalchemy
from worksystem.database.model.base import Base
from sqlalchemy import Column, String, Integer, Float

class Village(Base):
    __tablename__ = 'Village'
    # id 唯一标识符
    id = Column(Integer, primary_key=True)
    # 小区名字
    name = Column(String)
    # 地理位置
    location = Column(String)
    # 占地面积
    area_covery = Column(Float)
    # 开发商
    developer = Column(String)
    # 物业公司
    property_company = Column(String)