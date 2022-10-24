import flask,json

from services.user_service import UserService

class UserResource(object):


    def __init__(self):
        self.user_service = UserService()