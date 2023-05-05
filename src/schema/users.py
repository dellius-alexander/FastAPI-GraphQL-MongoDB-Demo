import json
import time
import traceback
from typing import Any, Dict

from graphene import (
    ObjectType,
    String,
    Schema,
    List,
    Field,
    InputObjectType,
    Mutation,
    relay,
    DateTime,
    Int
)
from graphene_mongo import MongoengineObjectType
from mongoengine import NotUniqueError, DoesNotExist
from models.Users import User
from utils.hash import check_password

# Get the logger
from myLogger.Logger import getLogger as GetLogger

# -----------------------------------------------------------------------------
log = GetLogger(__name__)


# -----------------------------------------------------------------------------
# Define the GraphQL schema object
class UserSchema(MongoengineObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)


# -----------------------------------------------------------------------------
# Define the GraphQL input object
class CreateUserInput(InputObjectType):
    name = String(required=True)
    email = String(required=True)
    password = String(required=True)
    age = Int(required=True)
    roles = List(
        String, default=["user"], description="List of roles assigned to user."
    )
    last_updated = DateTime(
        required=False,
        default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        description="Last update date.",
    )


# -----------------------------------------------------------------------------
# Define the GraphQL mutation
class CreateUserMutation(Mutation):
    user = Field(lambda: UserSchema)

    class Arguments:
        user_data = CreateUserInput(required=True)

    def mutate(self, info, user_data):
        try:
            log.info("user_data: %s" % json.dumps(user_data, indent=4))
            user = User.objects.get(email=user_data.email)
            user.name = user_data.name
            user.email = user_data.email
            user.password = user_data.password
            user.age = user_data.age
            user.roles = user_data.roles
            user.last_updated = user_data.last_updated
            user.save()
            ok = True
            log.info("user: %s" % json.dumps(user.to_json(), indent=4))
            return CreateUserMutation(user, ok)
        except NotUniqueError as e:
            return {"error": f"User with email {user.email} unable to be updated!\n{e}"}


# -----------------------------------------------------------------------------
# Define the GraphQL mutations
class UserMutations(ObjectType):
    create_user = CreateUserMutation.Field()


# -----------------------------------------------------------------------------
# Define the GraphQL schema
class Query(ObjectType):
    search = List(
        of_type=UserSchema,
        name=String(required=False),
        email=String(required=False),
        age=Int(required=False),
        roles=List(String, required=False),
    )

    delete_users = List(
        of_type=UserSchema,
        name=String(required=False),
        email=String(required=False),
        age=Int(required=False),
        roles=List(String, required=False),
    )

    create_users = List(
        of_type=UserSchema,
        name=String(),
        email=String(),
        password=String(),
        age=Int(),
        roles=List(String),
    )

    update_users = List(
        of_type=UserSchema,
        name=String(),
        email=String(),
        password=String(),
        age=Int(),
        roles=List(String),
    )

    def resolve_search(self, info, **kwargs):
        try:
            log.info("Keyword search: %s" % [kwargs.items()])
            query = {}
            if kwargs.get("name"):
                query["name"] = kwargs.get("name")
            if kwargs.get("email"):
                query["email"] = kwargs.get("email")
            if kwargs.get("age"):
                query["age"] = kwargs.get("age")
            if kwargs.get("roles"):
                query["roles"] = {"$in": kwargs.get("roles")}
            users_list = list(User.objects.filter(**query))
            log.info(
                "users_list: %s"
                % [
                    "".join(f"{k}: {v.__getstate__()['_data']}")
                    for k, v in enumerate(users_list)
                ]
            )
            return users_list
        except ConnectionError as e:
            # Handle MongoDB connection error
            raise Exception(f"Failed to connect to MongoDB: {e}")

    def resolve_create_users(self, info, name, email, password, age, roles=None):
        if roles is None:
            roles = ["user"]
        try:
            log.info(
                "New User: %s"
                % {
                    "name": name,
                    "email": email,
                    "password": password,
                    "age": age,
                    "roles": roles,
                }
            )
            new_user = User(
                name=name, email=email, password=password, age=age, roles=roles
            ).save()
            log.info(
                "New User Response: \n%s" % json.dumps(new_user.to_json(), indent=4)
            )
            if new_user:
                return [new_user]
        except (ConnectionError, DoesNotExist) as e:
            # Handle MongoDB connection error or user not found error
            raise Exception(f"Failed to create user: {e}")

    def resolve_delete_users(self, info, name=None, email=None, age=None, roles=None):
        try:
            query = {}
            if name:
                query["name"] = name
            if email:
                query["email"] = email
            if age:
                query["age"] = age
            if roles:
                query["roles"] = {"$in": roles}
            users_list = list(User.objects.filter(**query))
            log.info("users_list: %s" % users_list)
            status = list({})
            if len(users_list) > 0:
                for i, user in enumerate(users_list):
                    log.info("Deleting user: %s" % user.to_json())
                    response = user.delete()
                    if not response:
                        status.append({"Deleted": user.to_json()})
            else:
                status.append({"error": "No users found!"})
            log.info("status: %s" % status)
            return status
        except (ConnectionError, DoesNotExist) as e:
            # Handle MongoDB connection error
            log.error(
                f"Failed to connect to MongoDB: {e}",
                exc_info=traceback.format_exc(),
                stack_info=True,
            )

    def resolve_update_users(
        self, info, name=None, email=None, password=None, age=None, roles=None
    ):
        try:
            query = {}
            # if name:
            #     query["name"] = name
            if email:
                query["email"] = email
            # if age:
            #     query["age"] = age
            # if roles:
            #     query["roles"] = {"$in": roles}
            # if password:
            #     query["password"] = password
            users_list = list(User.objects.filter(**query))
            log.info("users_list: %s" % users_list)
            status = None
            if len(users_list) > 0:
                for i, user in enumerate(users_list):
                    log.info("Updating user: %s" % user.to_json())
                    if user.email == email:
                        user.name = name if name is not None and name != user.name else user.name
                        user.password = password if password is not None and not check_password(password, user.password) \
                            else user.password
                        user.age = age if age is not None and age != user.age else user.age
                        user.roles = roles if roles is not None and roles != user.roles else user.roles
                        status = user.update()
                    log.info("Response: %s" % status)
            else:
                status = {"errors": "No users found!"}
            log.info("status: %s" % status)
            return [status]
        except (ConnectionError, DoesNotExist) as e:
            # Handle MongoDB connection error
            log.error(
                f"Failed to connect to MongoDB: {e}",
                exc_info=traceback.format_exc(),
                stack_info=True,
            )


# -----------------------------------------------------------------------------
# Create the GraphQL schema
schema = Schema(query=Query, mutation=CreateUserMutation, types=[UserSchema])
# -----------------------------------------------------------------------------
