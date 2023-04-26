import json
import time
from graphene import ObjectType, String, Schema, List, Field, InputObjectType, Mutation, relay, DateTime, Int
from graphene_mongo import MongoengineObjectType
from mongoengine import NotUniqueError, DoesNotExist
from models.Users import User
from MyLogger import getLogger as GetLogger

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
    roles = List(String,
                 default=["user"],
                 description="List of roles assigned to user.")
    last_updated = DateTime(required=False,
                            default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                            description="Last update date.")


# -----------------------------------------------------------------------------
# Define the GraphQL mutation
class CreateUserMutation(Mutation):
    user = Field(lambda: UserSchema)

    class Arguments:
        user_data = CreateUserInput(required=True)

    def mutate(self, info, user_data=None):
        try:
            log.info(info)
            user = User(
                name=user_data.name,
                email=user_data.email,
                password=user_data.password,
                age=user_data.age,
                roles=user_data.roles,
                last_updated=user_data.last_update
            )
            result = user.save()
            log.info("result: %s" % result)
            if result:
                if user:
                    return f"User {user.name} created successfully!"
                else:
                    return f"User with email {user.email} already exists!"
            return CreateUserMutation(user=user)
        except NotUniqueError as e:
            return {"error": f"User with email {user.email} already exists!\n{e}"}


# -----------------------------------------------------------------------------
# Define the GraphQL mutations
class Mutation(ObjectType):
    create_user = CreateUserMutation.Field()


# -----------------------------------------------------------------------------
# Define the GraphQL schema
class Query(ObjectType):
    users = List(of_type=UserSchema,
                 name=String(required=False),
                 email=String(required=False),
                 age=Int(required=False),
                 roles=List(String, required=False)
                 )
    create_user = Field(type_=UserSchema,
                        name=String(),
                        password=String(),
                        email=String(),
                        age=Int(),
                        roles=List(String)
                        )

    def resolve_users(self, info, name=None, email=None, age=None, roles=None, **kwargs):
        try:
            query = {}
            if name:
                query['name'] = name
            if email:
                query['email'] = email
            if age:
                query['age'] = age
            if roles:
                query['roles'] = {'$in': roles}
            users_list = list(User.objects.filter(**query))
            # users_list = list(User.objects.all())
            log.info("users_list: %s" % users_list)
            return users_list
        except ConnectionError as e:
            # Handle MongoDB connection error
            raise Exception(f"Failed to connect to MongoDB: {e}")

    def resolve_create_user(self, info, name, email, password, age, roles, **kwargs):
        if roles is None:
            roles = ["user"]
        try:
            log.info("New User: %s" % {"name": name, "email": email, "password": password, "age": age, "roles": roles})
            new_user = User(
                name=name,
                email=email,
                password=password,
                age=age,
                roles=roles
            ).save()
            log.info("New User Response: %s" % [new_user.to_json()])
            if new_user:
                return new_user
            else:
                return new_user
        except (ConnectionError, DoesNotExist) as e:
            # Handle MongoDB connection error or user not found error
            raise Exception(f"Failed to create user: {e}")


# -----------------------------------------------------------------------------
# Create the GraphQL schema
schema = Schema(query=Query, mutation=CreateUserMutation, types=[UserSchema])
# -----------------------------------------------------------------------------
