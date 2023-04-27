import traceback

import pytest
import requests
import json

from models.Users import User as UserModel
from MyLogger import getLogger as GetLogger

log = GetLogger(__name__)

# -----------------------------------------------------------------------------
root_url = "http://localhost:8000"
user_url = root_url + "/user"


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
def test_delete_user():
    """
    Delete a user from the database
    """
    try:
        response = requests.post(
            url=user_url,
            json={"mutation": "{deleteUsers(email: \"jackie@example.com\"){name, email}}"},
            headers={"Content-Type": "application/json"},
            stream=True
        )
        assert response.status_code == 200
        print("\nResponse Status code: %s" % [response.status_code])
        print("\nResponse: %s" % response.json())
    except Exception as e:
        print("\nException: %s" % e)
        print("\nTraceback: %s" % traceback.format_exc())


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_root():
    """
    Test the root endpoint
    """
    print("Testing the root endpoint...")
    response = requests.get("http://localhost:8000/")
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
    request_body = {"query": "{users(email: \"brian@example.com\"){ name, email, age, password, lastUpdated }}"}
    # Execute the GraphQL query
    response = requests.post(
        url="http://0.0.0.0:8000/user",
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
    assert response.json()["data"]["users"] == [{'name': 'Brian Smith', 'email': 'brian@example.com', 'age': 39,
                                                 'password': '$2b$12$seD34UJYHJ4dopfjDhK1T.7vEh8Pt2k4XZZe/tTt3dh3gAuREiiKa',
                                                 'lastUpdated': '2023-04-26T08:47:37'}]


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_users():
    """
    Test the users endpoint
    """
    print("\nTesting the users endpoint...")
    # Execute the GraphQL query
    response = requests.post(
        url="http://0.0.0.0:8000/user",
        json={"query": "{users{ name, email, age }}"},
        headers={"Content-Type": "application/json"},
        stream=True
    )
    print("\nResponse Status code: %s" % [response.status_code])
    print("\nHeaders: %s" % response.headers)
    print("\nResponse: %s" % json.dumps(response.json(), indent=2))
    for user in response.json()["data"]["users"]:
        print("\nUser: %s" % user)
    assert response.status_code == 200
    assert response.json()["data"]["users"] == [
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
    request_body = {
        "query": "{createUser(name: \"Jackie Brown\", email: \"jackie@example.com\", password: \"jackie123\", age: 21, roles: [\"subscriber\",\"user\"]) { name, email, password, age, roles }}"}
    print("\nRequest body: %s" % request_body)
    # Execute the GraphQL query
    response = requests.post(
        url="http://0.0.0.0:8000/user",
        json=request_body,
        headers={"Content-Type": "application/json"},
        stream=True
    )
    verify = None
    if response.status_code == 200:
        # Verify the new user was created
        verify = requests.post(
            url="http://0.0.0.0:8000/user",
            json={"query": "{users(email: \"jackie@example.com\"){ name, email, password, age, roles }}"},
            headers={"Content-Type": "application/json"},
            stream=True
        )

    print("\nResponse Status code: %s" % [response.status_code])
    print("\nHeaders: %s" % response.headers)
    print("\nResponse: %s" % json.dumps(response.json()["data"], indent=2))
    print("\nVerify User Status code: %s" % [verify.status_code])
    print("\nVerify Headers: %s" % verify.headers)
    print("\nVerify Response: %s" % json.dumps(verify.json()["data"], indent=2))
    assert response.status_code == 200
    assert verify.status_code == 200
    assert response.json()["data"]["createUser"] == verify.json()["data"]["users"][0]
