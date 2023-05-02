import traceback

import bcrypt
from mongoengine.fields import StringField
from hash import hash_password
# Get the logger
from MyLogger.Logger import getLogger as GetLogger
log = GetLogger(__name__)


class PasswordField(StringField):
    """
    Encrypted password field
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_mongo(self, value):
        if isinstance(value, str):
            value = hash_password(value)
            return value
        return value
