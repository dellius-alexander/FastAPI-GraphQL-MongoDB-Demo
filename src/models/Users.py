import time
import traceback
from mongoengine import Document
from mongoengine.errors import (
    NotUniqueError,
    DoesNotExist,
    ValidationError,
    MongoEngineException,
)
from mongoengine.fields import (
    StringField,
    DateTimeField,
    IntField,
    EmailField,
    ListField,
)
from pydantic import BaseModel
from utils.hash import hash_password

# Get the logger
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)


# -----------------------------------------------------------------------------
# Define the model for a user
class User(Document):
    """
    User model for "users" collection
    """

    meta = {"db_alias": "default", "collection": "users"}
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    age = IntField(required=True)
    roles = ListField(StringField(), default=["user"])
    last_updated = DateTimeField(
        default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    )

    def save(self, *args, **kwargs):
        try:
            self.password = hash_password(self.password)
            return super(User, self).save(*args, **kwargs)
        except (
            MongoEngineException,
            ValidationError,
            NotUniqueError,
            DoesNotExist,
        ) as e:
            error = {
                "error": f"Email already exists. {e}",
                "traceback": f"{traceback.format_exc()}",
            }
            return error

    def update(self, *args, **kwargs):
        try:
            return super(User, self).save(*args, **kwargs)
        except (
            MongoEngineException,
            ValidationError,
            NotUniqueError,
            DoesNotExist,
        ) as e:
            error = {
                "error": f"{e}",
                "traceback": f"{traceback.format_exc()}",
            }
            return error

    def delete(self, **kwargs):
        try:
            return super(User, self).delete(**kwargs)
        except (
            MongoEngineException,
            ValidationError,
            NotUniqueError,
            DoesNotExist,
        ) as e:
            error = {
                "error": f"{e}",
                "traceback": f"{traceback.format_exc()}",
            }
            return error


# -----------------------------------------------------------------------------
class UserModel(BaseModel):
    """
    User model for "users" collection
    """

    id: str = None
    name: str = None
    email: str = None
    age: int = None
    roles: list = None
    last_updated: str = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Brian Smith",
                "email": "brian@example.com",
                "age": "39",
                "roles": ["admin", "user"],
                "last_updated": "2020-11-01 00:00:00",
            },
        }


# -----------------------------------------------------------------------------
