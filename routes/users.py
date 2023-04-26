# -----------------------------------------------------------------------------
import json
import traceback

from typing import Dict, Union, Any
from starlette.responses import JSONResponse
from main import app
from models.Response import JSONResponseModel
from models.Users import UserModel, User as UserAgent
from schema.Users import schema as user_schema, Query as UserQuery
from MyLogger import getLogger as GetLogger

# -----------------------------------------------------------------------------
log = GetLogger(__name__)


# -----------------------------------------------------------------------------
# Define the GraphQL endpoint
@app.post("/user",
          response_model=JSONResponseModel,
          status_code=200,
          tags=["user"],
          # dependencies=[Depends(use_cache=True)],
          summary="Get a user by query field(s).",
          description="Get a single user or a list of users",
          response_description="Retrieve User data",
          responses={
              200: {
                  "content": {"application/json": {
                      "example": [
                          {"id": "5f9f1b9b9b9b9b9b9b9b9b9b", "name": "Brian Smith", "email": "brian@example.com",
                           "age": 39, "roles": ["admin", "user"], "last_updated": "2020-11-01 00:00:00"}]}},
                  "description": "A single user or a list of users"},
              201: {
                  "content": {"application/json": {
                      "example": [
                          {"id": "5f9f1b9b9b9b9b9b9b9b9b9b", "name": "Brian Smith", "email": "brian@example.com",
                           "age": 39, "roles": ["admin", "user"], "last_updated": "2020-11-01 00:00:00"}]}},
                  "description": "Created a new user"},
              400: {"description": "Bad request"},
              404: {"description": "Not found"},
              500: {"description": "Internal server error"}
          },
          response_model_exclude_unset=True,
          # response_model_exclude={"description"},
          response_model_include={"id", "name", "email", "age", "roles"},
          response_model_by_alias=True,
          include_in_schema=True,
          response_class=JSONResponseModel,
          # openapi_extra=[]
          )
async def users(query: Union[Dict[str, Any]]) -> JSONResponse:
    """
    GraphQL endpoint for the user schema

    :param query: The GraphQL query
    :return: The result of the GraphQL query
    """
    log.info("Request: %s" % json.dumps(query, indent=2))
    # Insert some users
    if isinstance(query, Dict) and "query" in query or "mutation" in query:
        # Execute the GraphQL query
        result = await user_schema.execute_async(query["query"])
        log.info("Response: %s" % [result])
        # Return the result as a JSON response
        if result.errors:
            err = JSONResponse(
                content={"errors": [str(error) for error in result.errors], "msg": result.data},
                status_code=400,
                headers={"Content-Type": "application/json"}
            )
            log.error([err.body.decode("utf-8")],
                      exc_info=traceback.format_exc(),
                      stack_info=True)
            return err
        else:
            resp = JSONResponse(
                content={"data": result.data, "errors": result.errors},
                status_code=200,
                headers={"Content-Type": "application/json"},
                media_type="application/json"
            )
            log.info([resp.body.decode("utf-8")])
            return resp

# -----------------------------------------------------------------------------
