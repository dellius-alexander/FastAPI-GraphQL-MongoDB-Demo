import time
from mongoengine import Document
from mongoengine.errors import NotUniqueError
from mongoengine.fields import (
    StringField,
    DateTimeField,
    IntField,
    EmailField,
    ListField,
)
from pydantic import BaseModel
from MyLogger import getLogger as GetLogger
from utils.hash import hash_password

log = GetLogger(__name__)


# -----------------------------------------------------------------------------
# Define the model for a user
class User(Document):
    """
    User model for "users" collection
    """
    meta = {
        "db_alias": "default",
        "collection": "users"
    }
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    age = IntField(required=True)
    roles = ListField(StringField(), default=["user"])
    last_updated = DateTimeField(default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    def save(self, *args, **kwargs):
        try:
            self.password = hash_password(self.password)
            return super(User, self).save(*args, **kwargs)
        except NotUniqueError as e:
            return {"error": f"Email already exists. {e}"}


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
