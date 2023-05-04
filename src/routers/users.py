import json
import traceback
from typing import Dict, Union, Any
from starlette.responses import JSONResponse
from models.Response import JSONResponseModel
from schema.users import schema as user_schema

# Get the logger
from myLogger.Logger import getLogger as GetLogger
from fastapi import APIRouter, Depends

# -----------------------------------------------------------------------------
log = GetLogger(__name__)
router = APIRouter()


# -----------------------------------------------------------------------------
# Define the GraphQL endpoint
# -----------------------------------------------------------------------------


@router.post(
    path="/user",
    response_model=JSONResponseModel,
    status_code=200,
    tags=["query"],
    # dependencies=[Depends(use_cache=True)],
    summary="Get a user by query field(s).",
    description="Get a single user or a list of users",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "5f9f1b9b9b9b9b9b9b9b9b9b",
                            "name": "Brian Smith",
                            "email": "brian@example.com",
                            "age": 39,
                            "roles": ["admin", "user"],
                            "last_updated": "2020-11-01 00:00:00",
                        }
                    ]
                }
            },
            "description": "A single user or a list of users",
        },
        201: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "5f9f1b9b9b9b9b9b9b9b9b9b",
                            "name": "Brian Smith",
                            "email": "brian@example.com",
                            "age": 39,
                            "roles": ["admin", "user"],
                            "last_updated": "2020-11-01 00:00:00",
                        }
                    ]
                }
            },
            "description": "Created a new user",
        },
        400: {"description": "Bad request"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
    response_description="Retrieve User data",
    response_model_exclude_unset=True,
    # response_model_exclude={"password"},
    response_model_include={"id", "name", "email", "age", "roles"},
    response_model_by_alias=True,
    include_in_schema=True,
    response_class=JSONResponseModel,
    # openapi_extra=[]
)
async def query(_query: Union[Dict[str, Any]]) -> JSONResponse:
    """
    GraphQL endpoint for the user schema

    :param _query: The GraphQL query
    :return: The result of the GraphQL query
    """
    log.info("Request: %s" % json.dumps(_query, indent=2))
    # Insert some users
    if isinstance(_query, Dict) and "query" in _query:
        # Execute the GraphQL query
        result = await user_schema.execute_async(_query["query"])
        log.info("Response: %s" % result)
        # Return the result as a JSON response
        if result.errors:
            err = JSONResponse(
                content={
                    "errors": [str(error) for error in result.errors],
                    "msg": result.data,
                },
                status_code=404,
                headers={"Content-Type": "application/json"},
            )
            log.error([err.body], exc_info=traceback.format_exc(), stack_info=True)
            return err
        else:
            resp = JSONResponse(
                content={"data": result.data, "errors": result.errors},
                status_code=200,
                headers={"Content-Type": "application/json"},
                media_type="application/json",
            )
            log.info([resp.body.decode("utf-8")])
            return resp
    elif isinstance(_query, Dict) and "mutation" in _query:
        # Execute the GraphQL query
        result = await user_schema.execute_async(_query["mutation"])
        log.info("Response: %s" % result)
        # Return the result as a JSON response
        if result.errors:
            err = JSONResponse(
                content={
                    "errors": [str(error) for error in result.errors],
                    "msg": result.data,
                },
                status_code=404,
                headers={"Content-Type": "application/json"},
            )
            log.error(
                [err.body.decode("utf-8")],
                exc_info=traceback.format_exc(),
                stack_info=True,
            )
            return err
        else:
            resp = JSONResponse(
                content={"data": result.data, "errors": result.errors},
                status_code=200,
                headers={"Content-Type": "application/json"},
                media_type="application/json",
            )
            log.info([resp.body.decode("utf-8")])
            return resp


# -----------------------------------------------------------------------------
