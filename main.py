# Description: Main entry point for the application
# -----------------------------------------------------------------------------
import dotenv
import os
import uvicorn

# Load environment variables
dotenv.load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    verbose=True,
    encoding="utf-8"
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import connect_to_mongo, init_db
from MyLogger import getLogger as GetLogger

# -----------------------------------------------------------------------------
# Get the logger
log = GetLogger(__name__)
log.info("\n%s\nStarting the application...\nGlobals: \n%s\n%s", ("-" * 90), globals(), ("-" * 90))
# -----------------------------------------------------------------------------
# Create a FastAPI instance
app = FastAPI()

# Define the allowed origins for the CORS middleware
origins = ["http://localhost", "http://localhost", "https://example.com", "http://0.0.0.0", "http://127.0.0.1"]

# Enable the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
from routes.index import root
from routes.users import users


# -----------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    connect_to_mongo()
    init_db()
    log.info("API Routes: %s" % app.routes)
    log.info("Application started")
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Main entry point
if __name__ == "__main__":
    init_db()
    uvicorn.run(
        app,
        root_path="/",
        app_dir=os.path.dirname(__file__),
        host="0.0.0.0",
        port=8000,
        loop="auto",
        log_level="debug",
        reload=True,
        use_colors=True,
        env_file=os.path.join(os.path.dirname(__file__), ".env")
    )
