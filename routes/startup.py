from main import app
from database.db import connect_to_mongo, init_db
from MyLogger.Logger import getLogger as GetLogger
log = GetLogger(__name__)


# -----------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    connect_to_mongo()
    init_db()
    log.info("API Routes: %s" % app.routes)
    log.info("Application started")