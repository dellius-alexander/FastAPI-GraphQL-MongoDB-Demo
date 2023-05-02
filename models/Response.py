# Response models
# -----------------------------------------------------------------------------
from models.Users import UserModel
from starlette.responses import JSONResponse
# Get the logger
from MyLogger.Logger import getLogger as GetLogger
log = GetLogger(__name__)


# -----------------------------------------------------------------------------
class JSONResponseModel(JSONResponse, UserModel):
    """
    Collection class for response models

    - See: https://fastapi.tiangolo.com/tutorial/response-model/#response-types-that-match-a-model-will-be-passed-to-the-correct-models-response_class
    """
    pass


