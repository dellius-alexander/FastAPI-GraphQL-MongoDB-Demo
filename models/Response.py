# Response models
# -----------------------------------------------------------------------------
from models.Users import UserModel
from starlette.responses import JSONResponse


# -----------------------------------------------------------------------------
class JSONResponseModel(JSONResponse, UserModel):
    """
    Collection class for response models

    - See: https://fastapi.tiangolo.com/tutorial/response-model/#response-types-that-match-a-model-will-be-passed-to-the-correct-models-response_class
    """
    pass


