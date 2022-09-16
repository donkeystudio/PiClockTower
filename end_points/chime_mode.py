

from clock_tower import ClockTower
from model.credential import Credential
from server.api_server import AuthResource
from flask_restful.reqparse import RequestParser


class ChimeMode(AuthResource):
    
    clock = None
    allowed_get_mode   = ["query"]
    allowed_post_mode  = ["update"]
    allowed_action = ['on', 'off']
    request_parser = RequestParser()

    def __init__(self) -> None:
        super().__init__()
        self.request_parser.add_argument('mode', default='', location='args')
        self.request_parser.add_argument('action', default='off', location='args')

    def get(self):
        return self.process_requests(self.allowed_get_mode)

    def post(self):
        return self.process_requests(self.allowed_post_mode)

    def process_requests(self, allowed_mode):
        #Get request parameter
        args = self.request_parser.parse_args()
        mode = args['mode'].lower()
        self._logger.info(f'Mode is {mode}')

        if mode not in allowed_mode:
            return {'result': 403, 'message': 'Invalid Mode'}, 403
        else:
            if mode != 'query':
                action = args['action'].lower()
                self._logger.info(f'Action is {action}')
                if action not in self.allowed_action:
                    return {'result': 403, 'message': 'Invalid Action'}, 403
                ChimeMode.clock.set_quiet_time(action == 'off')
            
            status = ChimeMode.clock.is_quiet_time and 'quiet' or 'chime'
            return {'result': 200,  'status': f'{status}'}, 200

    @AuthResource.auth.verify_password
    def verify_password(username, password):
        if ChimeMode.credential.get_username() is None and ChimeMode.credential.get_password() is None:
            return True
        if username == ChimeMode.credential.get_username() and password == ChimeMode.credential.get_password():
            return True
        return False