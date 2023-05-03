#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import requests
import json
from src.myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)


# -----------------------------------------------------------------------------
root_url = "http://127.0.0.1:8000"
user_url = root_url + "/user"
print("\nroot_url: %s" % root_url)
print("\nuser_url: %s" % user_url)
log.info("root_url: %s" % root_url)
log.info("user_url: %s" % user_url)

# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def entity_exist(email) -> bool:
    log.info(f"Checking if {email} entity exists in the database...")
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
            log.info(f"{email} entity does not exist in the database!")
            return False
        else:
            log.info(f"{email} entity exists in the database!")
            return True
    else:
        print("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def delete_entity(email) -> bool:
    log.info(f"Deleting {email} entity from the database...")
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
            log.info(f"{email} entity does not exist in the database!")
            return True
        else:
            log.info(f"{email} entity exists in the database!")
            return False
    else:
        print("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def root():
    """
    Test the root endpoint
    """
    log.info("Testing the root endpoint...")
    print("Testing the root endpoint...")
    response = requests.get(
        url=root_url
    )
    assert response.status_code == 200
    # assert response.json() == {"message": "Hello, World!"}
    print("\nResponse Status code: %s" % [response.status_code])
    print("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def user():
    """
    Test the user endpoint
    """
    log.info("Testing the user endpoint...")
    print("\nTesting the user endpoint...")
    request_body = {"query": "{search(email: \"brian@example.com\"){ name, email, age }}"}
    log.info(f"request_body: {request_body}")
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
        log.info(f"Response: {response.json()}")
        print("\nResponse: %s" % response.json())
        assert response.status_code == 200
        assert response.json()["data"]["search"] == [{'name': 'Brian Smith', 'email': 'brian@example.com', 'age': 39}]

    else:
        log.info(f"Response: {response.text}")
        print("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def users():
    """
    Test the users endpoint
    """
    log.info("Testing the users endpoint...")
    print("\nTesting the users endpoint...")
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json={"query": "{search{ name, email, age }}"},
        headers={"Content-Type": "application/json"},
        stream=True
    )
    if response.status_code == 200:
        log.info(f"Response: {response.json()}")
        print("\nResponse Status code: %s" % [response.status_code])
        print("\nHeaders: %s" % response.headers)
        print("\nResponse: %s" % json.dumps(response.json(), indent=4))
        for user in response.json()["data"]["search"]:
            print("\nUser: %s" % user)
            log.info(f"User: {user}")
        assert response.status_code == 200
        assert response.json()["data"]["search"][:6] == [
            {'name': 'Brian Smith', 'email': 'brian@example.com', 'age': 39},
            {'name': 'John Doe', 'email': 'john@example.com', 'age': 25},
            {'name': 'Jane Doe', 'email': 'jane@example.com', 'age': 27},
            {'name': 'Alice Jones', 'email': 'alice@example.com', 'age': 23},
            {'name': 'Bob Smith', 'email': 'bob@example.com', 'age': 24},
            {'name': 'James Cook', 'email': 'james@example.com', 'age': 29}
        ]
    else:
        print("\nResponse Status code: %s" % [response.status_code])
        print("\nHeaders: %s" % response.headers)
        print("\nResponse: %s" % response.text)
        log.info(f"Response: {response.text}")


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def create_user():
    """
    Test the create user endpoint
    """
    log.info("Testing the create_user endpoint...")
    print("\nTesting the create user endpoint...")
    # check if entity exists in the database and delete it if it does exist already before creating it again.
    if await entity_exist("jackie@example.com") and await delete_entity("jackie@example.com"):
        print("\nUser already exists and deleted...")
    else:
        print("\nUser does not exist...")
    request_body = {
        "query": "{createUsers(name: \"Jackie Brown\", email: \"jackie@example.com\", password: \"jackie123\", age: 21, roles: [\"subscriber\",\"user\"]) { name, email, password, age, roles }}"}
    log.info(f"request_body: {request_body}")
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
        log.info(f"Response: {response.json()}")
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
            log.info(f"Response: {verify.json()}")
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


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_run_all():
    """
    Run all tests
    """
    await root()
    await user()
    await users()
    await create_user()


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
