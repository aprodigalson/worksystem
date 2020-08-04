import wsgiref.simple_server as wsg
from pecan import make_app

server = {
    'port': '9000',
    'host': '0.0.0.0'
}

app = {
    'root': 'worksystem.api.server.controllers.root.RootController',
    'debug': False
}


def application():
    return make_app(app.pop('root'), **app)


def run_wsgi():
    ser = wsg.make_server(server['host'], int(server['port']), application())
    ser.serve_forever()


if __name__ == '__main__':
    run_wsgi()
