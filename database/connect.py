import logging
import traceback

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from worksystem.database.config import default_sqlite_config

from worksystem.database.model.base import Base
from worksystem.database.model.person import Owner


class DbUtils(object):
    __engine = create_engine(default_sqlite_config.get('url'))
    Base.metadata.bind = __engine
    Base.metadata.create_all()
    __Session = sessionmaker(bind=__engine)
    __session = __Session()

    @classmethod
    def get_session(cls):
        return cls.__session

    @classmethod
    def add_item(cls, item):
        try:
            cls.__session.add(item)
            cls.__session.commit()
            return True
        except Exception:
            logging.warning(traceback.format_exc())
            return False

    @classmethod
    def delete_item(cls, item):
        try:
            cls.__session.delete(item)
            cls.__session.commit()
            return True
        except Exception:
            logging.warning(traceback.format_exc())
            return False

    @classmethod
    def get_all(cls, bean):
        if not isinstance(bean, DeclarativeMeta):
            logging.error('error table type')
            return []
        res = cls.__session.query(bean).all()
        return res

    @classmethod
    def delete_all_table(cls):
        Base.metadata.drop_all(cls.__engine)

    @classmethod
    def delete_table(cls, model):
        model.__table__.drop()


if __name__ == '__main__':
    # DbUtils.delete_all_table()
    # DbUtils.delete_table(Owner)
    all_list = DbUtils.get_all(Owner)
    print(all_list)
