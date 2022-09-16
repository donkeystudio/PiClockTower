import logging
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource
from model.credential import Credential


class AuthResource(Resource):
    ''' Resource class with HTTP Basic Authentication supported
    '''

    __name__ = 'AuthResource'
    auth = HTTPBasicAuth()
    credential = Credential()
    _logger = logging.getLogger(__name__)

    method_decorators = {
        'get': [auth.login_required],
        'post': [auth.login_required]
    }

    def get(self):
        return {'result': 501, 'message': 'Method not supported'}, 501
    
    def post(self):
        return {'result': 501, 'message': 'Method not supported'}, 501

    @auth.verify_password
    def verify_password(username, password):
        if AuthResource.credential.get_username() is None and AuthResource.credential.get_password() is None:
            return True
        if username == AuthResource.credential.get_username() and password == AuthResource.credential.get_password():
            return True
        return False


class APIServer:
    app: Flask
    api: Api

    def __init__(self, app_name) -> None:
        self.app = Flask(app_name)
        self.api = Api(self.app)

    def add_resource(self, route: str, resource_class, **args):
        self.api.add_resource(resource_class, route, **args)

    def start(self, host: str, port: int, **kwargs):
        self.app.run(debug = False, host = host, port = port)