from starlette.responses import JSONResponse
from typing import List


class UserResponse(JSONResponse):
    id: str
    name: str
    email: str
    age: str
    roles: List[str]
    last_updated: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "age": "29",
                "roles": ["user", "subscriber"],
                "last_updated": "2020-02-01 00:00:00",
            },
        }
