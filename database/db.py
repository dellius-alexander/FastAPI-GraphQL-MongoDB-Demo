import json
import time
import traceback
from mongoengine import connect, ConnectionFailure
import os
from mongoengine import Document
from models.Users import User as UserModel
from MyLogger import getLogger

log = getLogger(__name__)
# Get the port from the environment variables
MONGODB_USERNAME = os.getenv("APP_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_PORT = os.getenv("MONGODB_PORT")


def connect_to_mongo():
    try:
        connect(
            # the name of the database to use, for compatibility with connect
            db="Hyfi",
            # the host name of the: program: mongod instance to connect to
            # f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_IP_PORT}/{MONGODB_DATABASE}",
            host=f'mongodb://{MONGODB_URL}:{MONGODB_PORT}/{MONGODB_DATABASE}',
            # the name that will be used to refer to this connection throughout MongoEngine
            alias="default",
            # the name of the specific database to use
            name=MONGODB_DATABASE,
            # the port that the: program: mongod instance is running on
            port=int(MONGODB_PORT),
            # # The read preference for the collection
            # read_preference=None,
            # username to authenticate with
            username=MONGODB_USERNAME,
            # password to authenticate with
            password=MONGODB_PASSWORD,
            # database to authenticate against
            authentication_source=MONGODB_DATABASE,
            # # database authentication mechanisms. By default, use SCRAM-SHA-1 with MongoDB 3.0 and later,
            # # MONGODB-CR (MongoDB Challenge Response protocol) for older servers.
            # authentication_mechanism=None,
            # # using alternative connection client other than pymongo.MongoClient, e.g. mongomock, montydb,
            # # that provides pymongo alike interface but not necessarily for connecting to a real mongo instance.
            # mongo_client_class=None,
            # # ad-hoc parameters to be passed into the pymongo driver, for example maxpoolsize, tz_aware, etc.
            # # See the documentation for pymongo’s MongoClient for a full list.
            # kwargs=None,
        )
        log.info("Connected to MongoDB")
        # The ping command is cheap and does not require auth.
        # client.admin.command('ping')
    except ConnectionFailure as e:
        log.error("Server not available.")
        log.error(e,
                  exc_info=traceback.format_exc(),
                  stack_info=True)


def init_db():
    try:
        log.info("\nInitializing the database with demo user data, for use with testing and querying...\n")
        # Create the fixtures
        brian = UserModel(
            name="Brian Smith",
            password="brian123",
            email="brian@example.com",
            age=39,
            roles=["admin", "user"]
        )
        brian.save()

        john = UserModel(
            name="John Doe",
            password="john123",
            email="john@example.com",
            age=25,
            roles=["subscriber", "user"]
        )
        john.save()

        jane = UserModel(
            name="Jane Doe",
            password="jane123",
            email="jane@example.com",
            age=27,
            roles=["subscriber", "user"]
        )
        jane.save()

        alice = UserModel(
            name="Alice Jones",
            password="alice123",
            email="alice@example.com",
            age=23,
            roles=["subscriber", "user"]
        )
        alice.save()

        bob = UserModel(
            name="Bob Smith",
            password="bob123",
            email="bob@example.com",
            age=24,
            roles=["subscriber", "user"]
        )
        bob.save()

        james = UserModel(
            name="James Cook",
            password="james123",
            email="james@example.com",
            age=29,
            roles=["subscriber", "user"]
        )
        james.save()

        for user in UserModel.objects[:1]:
            log.info(
                "%s" %
                json.dumps(
                    user.to_json(),
                    indent=4,
                    sort_keys=True,
                    allow_nan=True,
                    ensure_ascii=True
                )
            )
    except Exception as e:
        log.error(e,
                  exc_info=traceback.format_exc(),
                  stack_info=True)
