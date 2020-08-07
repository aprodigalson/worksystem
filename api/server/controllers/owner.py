from pecan import expose
from worksystem.database.dao.owner import OwnerProcess

class OwnerController(object):

    @expose()
    def index(self):
        pass

    #@index.when(method='GET')
    @expose(method='GET')
    def get(self):
        return OwnerProcess.show_all_owner()

    @expose(method='GET')
    def add(self):
        return OwnerProcess.add_random_owner()

