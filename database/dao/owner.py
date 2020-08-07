from worksystem.database.connect import DbUtils
from worksystem.database.model.owner import Owner


class OwnerProcess(object):
    # select
    # add
    # delete
    session = DbUtils.get_session()
    @classmethod
    def add_owner(cls, owner):
        if isinstance(owner, Owner):
            DbUtils.add_item(owner)

    def delete_owner(self, owner):
        if isinstance(owner, Owner):
            DbUtils.delete_item(owner)

    @classmethod
    def select_owner_by_name(cls, name):
        data = cls.session.query(Owner).filter(Owner.name == name).all()
        print(data)
        return data

    @classmethod
    def get_all_owner(cls):
        return DbUtils.get_all(Owner)

    @classmethod
    def show_all_owner(cls):
        owners = cls.get_all_owner()
        result = ''
        for owner in owners:
            tmp_owner = 'id: %s, name: %s, role:%s \n'% (owner.id, owner.name, owner.role)
            print(tmp_owner)
            result += tmp_owner
        return result
    # test_interface

    @classmethod
    def add_random_owner(cls):
        import random
        from worksystem.common.utils import StringUtils
        DbUtils.add_item(Owner(id=random.randint(1, 1000), name=StringUtils.random_string(5), role='业主'))


if __name__ == '__main__':
    OwnerProcess.add_random_owner()
    OwnerProcess.show_all_owner()

