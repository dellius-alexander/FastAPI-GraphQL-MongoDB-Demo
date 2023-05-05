#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import requests
import json
from src.myLogger.Logger import getLogger as GetLogger
log = GetLogger(__name__)


# -----------------------------------------------------------------------------
root_url = "http://0.0.0.0:8000"
user_url = root_url + "/user"
log.debug("\nroot_url: %s" % root_url)
log.debug("\nuser_url: %s" % user_url)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def entity_exist(email) -> bool:
    """
    Check if an entity exists in the database
    :param email: The email of the entity to check
    :return: True if the entity exists, False otherwise
    """
    log.debug(f"Checking if {email} entity exists in the database...")
    # check if entity exists in the database
    request_body = {"query": "{search(email: \"%s\"){ name, email, age }}" % email}
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json=request_body,
        headers={"Content-Type": "application/json"},
        stream=True
    )
    log.debug("\nResponse Status code: %s" % [response.status_code])
    log.debug("\nHeaders: %s" % response.headers)
    if response.status_code == 200:
        log.debug("\nResponse: %s" % response.json())
        if not response.json()["data"]["search"]:
            log.debug(f"{email} entity does not exist in the database!")
            return False
        else:
            log.debug(f"{email} entity exists in the database!")
            return True
    else:
        log.debug("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def delete_entity(email) -> bool:
    """
    Delete an entity from the database
    :param email: The email of the entity to delete
    :return: True if the entity was deleted, False otherwise
    """
    log.debug(f"Deleting {email} entity from the database...")
    # delete entity from the database
    request_body = {"mutation": "{deleteUsers(email: \"%s\"){ name, email, age }}" % email}
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json=request_body,
        headers={"Content-Type": "application/json"},
        stream=True
    )
    log.debug("\nResponse Status code: %s" % [response.status_code])
    log.debug("\nHeaders: %s" % response.headers)
    if response.status_code == 200:
        log.debug("\nResponse: %s" % response.json())
        if not response.json()["data"]["deleteUsers"]:
            log.debug(f"{email} entity does not exist in the database!")
            return True
        else:
            log.debug(f"{email} entity exists in the database!")
            return False
    else:
        log.debug("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_root():
    """
    Test the root endpoint
    """
    log.debug("Testing the root endpoint...")
    response = requests.get(
        url=root_url
    )
    assert response.status_code == 200
    # assert response.json() == {"message": "Hello, World!"}
    log.debug("\nResponse Status code: %s" % [response.status_code])
    log.debug("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_user():
    """
    Test the user endpoint
    """
    log.debug("\nTesting the user endpoint...")
    request_body = {"query": "{search(email: \"brian@example.com\"){ name, email, age }}"}
    log.debug(f"request_body: {request_body}")
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json=request_body,
        headers={"Content-Type": "application/json"},
        stream=True
    )
    log.debug("\nResponse Status code: %s" % [response.status_code])
    log.debug("\nHeaders: %s" % response.headers)
    if response.status_code == 200:
        log.debug("\nResponse: %s" % response.json())
        assert response.status_code == 200
        assert response.json()["data"]["search"] == [{'name': 'Brian Smith', 'email': 'brian@example.com', 'age': 39}]

    else:
        log.debug("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_query_users():
    """
    Test the users endpoint
    """
    log.debug("\nTesting the users endpoint...")
    # Execute the GraphQL query
    response = requests.post(
        url=user_url,
        json={"query": "{search{ name, email, age }}"},
        headers={"Content-Type": "application/json"},
        stream=True
    )
    if response.status_code == 200:
        log.debug("\nResponse Status code: %s" % [response.status_code])
        log.debug("\nHeaders: %s" % response.headers)
        log.debug("\nResponse: %s" % json.dumps(response.json(), indent=4))
        for user in response.json()["data"]["search"]:
            log.debug("\nUser: %s" % user)
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
        log.debug("\nResponse Status code: %s" % [response.status_code])
        log.debug("\nHeaders: %s" % response.headers)
        log.debug("\nResponse: %s" % response.text)


# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_user():
    """
    Test the create user endpoint
    """
    log.debug("\nTesting the create user endpoint...")
    # check if entity exists in the database and delete it if it does exist already before creating it again.
    if await entity_exist("jackie@example.com") and await delete_entity("jackie@example.com"):
        log.debug("\nUser already exists and deleted...")
    else:
        log.debug("\nUser does not exist...")
    request_body = {
        "query": "{createUsers(name: \"Jackie Brown\", email: \"jackie@example.com\", password: \"jackie123\", age: 21, roles: [\"subscriber\",\"user\"]) { name, email, password, age, roles }}"
    }
    log.debug("\nRequest body: %s" % request_body)
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
        log.debug("\nCreation Response Status code: %s" % [response.status_code])
        log.debug("\nCreation Headers: %s" % response.headers)
        log.debug("\nCreation Response: %s" % response.json())

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

            log.debug("\nVerify Response Status code: %s" % [verify.status_code])
            log.debug("\nVerify Headers: %s" % verify.headers)
            log.debug("\nVerify Response: %s" % json.dumps(verify.json()["data"], indent=4))
        else:
            log.debug("\nVerify Response: %s" % verify.text)
    else:
        log.debug("\nCreation Response: %s" % response.text)


# -----------------------------------------------------------------------------
# @pytest.mark.asyncio
# async def test_run_all():
#     """
#     Run all tests
#     """
#     await test_root()
#     await test_user()
#     await test_query_users()
#     await test_create_user()


