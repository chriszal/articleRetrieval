import commons.constants as constants

import mongoengine as mongo
from resource.user_resource import UserResource

mongo.connect(
    constants.MONGO['DATABASE'],
    host=constants.MONGO['HOST'],
    port=constants.MONGO['PORT'],
    username=constants.MONGO['USERNAME'],
    password=constants.MONGO['PASSWORD']
)

user=UserResource()
