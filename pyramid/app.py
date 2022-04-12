from wsgiref.simple_server import make_server
from pyramid.config import Configurator


if __name__ == "__main__":
    with Configurator() as config:
        config.add_route('redirect', '/goto')
        config.add_route('refreshaccess', '/refresh')
        config.add_route('revoke', '/revoke')
        config.add_route('createmeeting', '/createmeeting')
        config.add_route('listmeeting', '/listmeeting')
        config.add_route('delete', '/delete')
        config.add_route('recording', '/recording')
        config.scan('views')
        config.include ('pyramid_chameleon')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()