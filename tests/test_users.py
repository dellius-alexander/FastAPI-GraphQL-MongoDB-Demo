import traceback
import pytest
import requests
import json
from MyLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)

# -----------------------------------------------------------------------------
root_url = "http://0.0.0.0:8000"
user_url = root_url + "/user"

log.info("root_url: %s" % root_url)
log.info("user_url: %s" % user_url)


# -----------------------------------------------------------------------------
async def entity_exist(email) -> bool:
    # check if entity exists in the database
    request_body = {"query": "{search(email: \"%s\"){ name, email, age }}" % email}
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json=request_body,
        headers={"Content-Type": "application/json"},
        stream=True
    )
    print("\nResponse Status code: %s" % [response.status_code])
    print("\nHeaders: %s" % response.headers)
    if response.status_code == 200:
        print("\nResponse: %s" % response.json())
        if not response.json()["data"]["search"]:
            return False
        else:
            return True
    else:
        print("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
async def delete_entity(email) -> bool:
    # delete entity from the database
    request_body = {"mutation": "{deleteUsers(email: \"%s\"){ name, email, age }}" % email}
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json=request_body,
        headers={"Content-Type": "application/json"},
        stream=True
    )
    print("\nResponse Status code: %s" % [response.status_code])
    print("\nHeaders: %s" % response.headers)
    if response.status_code == 200:
        print("\nResponse: %s" % response.json())
        if not response.json()["data"]["deleteUsers"]:
            return True
        else:
            return False
    else:
        print("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_root():
    """
    Test the root endpoint
    """
    print("Testing the root endpoint...")
    response = requests.get(root_url)
    assert response.status_code == 200
    # assert response.json() == {"message": "Hello, World!"}
    print("\nResponse Status code: %s" % [response.status_code])
    print("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_user():
    """
    Test the user endpoint
    """
    print("\nTesting the user endpoint...")
    request_body = {"query": "{search(email: \"brian@example.com\"){ name, email, age }}"}
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json=request_body,
        headers={"Content-Type": "application/json"},
        stream=True
    )
    print("\nResponse Status code: %s" % [response.status_code])
    print("\nHeaders: %s" % response.headers)
    if response.status_code == 200:
        print("\nResponse: %s" % response.json())
    else:
        print("\nResponse: %s" % response.text)
    assert response.status_code == 200
    assert response.json()["data"]["search"] == [{'name': 'Brian Smith', 'email': 'brian@example.com', 'age': 39}]


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_users():
    """
    Test the users endpoint
    """
    print("\nTesting the users endpoint...")
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json={"query": "{search{ name, email, age }}"},
        headers={"Content-Type": "application/json"},
        stream=True
    )
    print("\nResponse Status code: %s" % [response.status_code])
    print("\nHeaders: %s" % response.headers)
    print("\nResponse: %s" % json.dumps(response.json(), indent=4))
    for user in response.json()["data"]["search"]:
        print("\nUser: %s" % user)
    assert response.status_code == 200
    assert response.json()["data"]["search"][:6] == [
        {'name': 'Brian Smith', 'email': 'brian@example.com', 'age': 39},
        {'name': 'John Doe', 'email': 'john@example.com', 'age': 25},
        {'name': 'Jane Doe', 'email': 'jane@example.com', 'age': 27},
        {'name': 'Alice Jones', 'email': 'alice@example.com', 'age': 23},
        {'name': 'Bob Smith', 'email': 'bob@example.com', 'age': 24},
        {'name': 'James Cook', 'email': 'james@example.com', 'age': 29}
    ]


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_user():
    """
    Test the create user endpoint
    """
    print("\nTesting the create user endpoint...")
    # check if entity exists in the database and delete it if it does exist already before creating it again.
    if await entity_exist("jackie@example.com") and await delete_entity("jackie@example.com"):
        print("\nUser already exists and deleted...")
    else:
        print("\nUser does not exist...")
    request_body = {
        "query": "{createUsers(name: \"Jackie Brown\", email: \"jackie@example.com\", password: \"jackie123\", age: 21, roles: [\"subscriber\",\"user\"]) { name, email, password, age, roles }}"}
    print("\nRequest body: %s" % request_body)
    # Execute the GraphQL query to create a new user
    response = requests.post(
        url=user_url,
        json=request_body,
        headers={"Content-Type": "application/json"},
        stream=True
    )
    # Verify the response for the new user creation
    if response.status_code == 200:
        assert response.status_code == 200
        print()
        print("\nCreation Response Status code: %s" % [response.status_code])
        print("\nCreation Headers: %s" % response.headers)
        print("\nCreation Response: %s" % response.json())
        # Verify the new user was created and exists in the database, then retrieve the new user
        verify = requests.post(
            url=user_url,
            json={"query": "{search(email: \"jackie@example.com\"){ name, email, password, age, roles }}"},
            headers={"Content-Type": "application/json"},
            stream=True
        )
        # Verify the response for the new user creation
        if verify.status_code == 200:
            assert verify.status_code == 200
            assert response.json()["data"]["createUsers"][0] == verify.json()["data"]["search"][0]
            print()
            print("\nVerify Response Status code: %s" % [verify.status_code])
            print("\nVerify Headers: %s" % verify.headers)
            print("\nVerify Response: %s" % json.dumps(verify.json()["data"], indent=4))
        else:
            print("\nVerify Response: %s" % verify.text)
    else:
        print("\nCreation Response: %s" % response.text)


# # -----------------------------------------------------------------------------
# @pytest.mark.asyncio
# async def test_delete_user():
#     """
#     Delete a user from the database
#     """
#     try:
#         response = requests.post(
#             url=user_url,
#             json={"mutation": "{deleteUsers(email: \"jackie@example.com\"){name, email}}"},
#             headers={"Content-Type": "application/json"},
#             stream=True
#         )
#         assert response.status_code == 200
#         print("\nResponse Status code: %s" % [response.status_code])
#         print("\nResponse: %s" % response.json())
#     except Exception as e:
#         print("\nException: %s" % e)
#         print("\nTraceback: %s" % traceback.format_exc())

