from database.db import connect_to_mongo, init_db
from myLogger.Logger import getLogger as GetLogger
from fastapi import APIRouter

# -----------------------------------------------------------------------------
log = GetLogger(__name__)
event = APIRouter()


# -----------------------------------------------------------------------------
@event.on_event("startup")
async def startup_event():
    connect_to_mongo()
    init_db()
