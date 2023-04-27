from models.Users import UserModel as User
from schema.Users import Query
from graphene import relay, ObjectType
# Get the logger
from MyLogger.Logger import getLogger as GetLogger
log = GetLogger(__name__)


class UserType(ObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
