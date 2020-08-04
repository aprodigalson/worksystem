from pecan import expose


class OwnerController(object):

    @expose(generic=True)
    def index(self):
        pass

    @index.when(method='GET')
    def get(self):
        return 'get'
