from pecan import expose
from worksystem.api.server.controllers.owner import OwnerController


class V1Controller(object):
    owner = OwnerController()

    @expose()
    def index(self):
        return 'v1'


class RootController(object):
    v1 = V1Controller()

    @expose()
    def index(self):
        return 'hell0'
