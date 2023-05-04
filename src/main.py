# Description: Main entry point for the application
# -----------------------------------------------------------------------------
import argparse
import traceback
import dotenv
import os
import uvicorn

# Load environment variables
dotenv.load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env")
    or dotenv.find_dotenv(".env", False, False),
    verbose=True,
    encoding="utf-8",
)

dotenv.find_dotenv(".env")

# -----------------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Get the logger
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)

# -----------------------------------------------------------------------------
log.info(
    "\n%s\nStarting the application...\nGlobals: \n%s\n%s",
    ("-" * 90),
    globals(),
    ("-" * 90),
)
# -----------------------------------------------------------------------------
# Create a FastAPI instance
app = FastAPI()
# -----------------------------------------------------------------------------
# Define the allowed origins for the CORS middleware
origins = [
    "http://localhost",
    "http://localhost",
    "https://example.com",
    "http://0.0.0.0",
    "http://127.0.0.1",
]
# -----------------------------------------------------------------------------
# Enable the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Add the routes
from routers import startup, index, users

app.add_event_handler("startup", startup.startup_event)
app.include_router(index.router)
app.include_router(users.router)


log.info("API Routes: %s" % app.routes)
log.info("Application started")
# -----------------------------------------------------------------------------
# Generate the OpenAPI Schema and save to file: api-docs/openapi.yaml
openapi_schema = app.openapi()
openapi_schema["info"]["title"] = "FastAPI, GraphQL, MongoDB Demo API"
openapi_schema["info"]["version"] = "0.0.1"
openapi_schema["info"][
    "description"
] = "This is a demo API for FastAPI, GraphQL, MongoDB"


# -----------------------------------------------------------------------------
def get_parser():
    """
    Generate a parameters parser.
    """
    import ssl

    # SSL_PROTOCOL_VERSION = os.getenv("SSL_PROTOCOL_VERSION", "TLSv1_2")
    parser = argparse.ArgumentParser(description="Uvicorn run function")

    # Application-related arguments
    parser.add_argument(
        "--app", type=str, default="main:app", help="Application to run"
    )

    # Host and port options
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    # parser.add_argument("--uds", type=str, help="Unix domain socket to bind to")
    # parser.add_argument("--fd", type=int, help="File descriptor to bind to")
    parser.add_argument("--loop", type=str, default="auto", help="Event loop to use")

    # Protocol implementation options
    parser.add_argument(
        "--http", type=str, default="auto", help="HTTP implementation to use"
    )
    parser.add_argument(
        "--ws", type=str, default="auto", help="WebSocket implementation to use"
    )
    parser.add_argument(
        "--ws-max-size", type=int, default=16777216, help="Max WebSocket message size"
    )
    parser.add_argument(
        "--ws-ping-interval", type=float, default=20.0, help="WebSocket ping interval"
    )
    parser.add_argument(
        "--ws-ping-timeout", type=float, default=20.0, help="WebSocket ping timeout"
    )
    parser.add_argument(
        "--ws-per-message-deflate",
        type=bool,
        default=True,
        help="Enable/disable WebSocket per-message deflate",
    )

    # Lifespan related options
    parser.add_argument(
        "--lifespan", type=str, default="auto", help="Lifespan implementation to use"
    )

    # Application interface options
    parser.add_argument(
        "--interface", type=str, default="auto", help="Application interface to use"
    )

    # Reloader options
    parser.add_argument(
        "--reload", type=bool, default=True, help="Enable/disable code reloader"
    )
    parser.add_argument(
        "--reload-dirs",
        type=str,
        default="..",
        help="Folders to watch for code changes",
    )
    # parser.add_argument("--reload-includes", type=list, default=["logging.json"],
    #                     help="Files to watch for code changes")
    # parser.add_argument("--reload-excludes", type=list, default=["docker-compose.yml"],
    #                     help="Files to exclude from code changes")
    parser.add_argument(
        "--reload-delay",
        type=float,
        default=0.25,
        help="Delay between code change checks",
    )

    # Worker options
    parser.add_argument(
        "--workers", type=int, default=2, help="Number of workers to use"
    )
    parser.add_argument(
        "--env-file",
        type=str,
        default=os.path.join(os.path.dirname(__file__), ".env"),
        help="Path to a .env file",
    )

    # Logging options
    parser.add_argument(
        "--log-config",
        type=str,
        default="logging.json",
        help="Logging config file to use",
    )
    parser.add_argument(
        "--log-level", type=str, default="debug", help="Logging level to use"
    )
    parser.add_argument(
        "--access-log", type=bool, default=True, help="Enable/disable access log"
    )

    # HTTP server options
    parser.add_argument(
        "--proxy-headers", type=bool, default=True, help="Enable/disable proxy headers"
    )
    parser.add_argument(
        "--server-header", type=bool, default=True, help="Enable/disable server header"
    )
    parser.add_argument(
        "--date-header", type=bool, default=True, help="Enable/disable date header"
    )
    parser.add_argument(
        "--forwarded-allow-ips",
        type=str,
        default="127.0.0.1",
        help="IP addresses to allow in forwarded headers",
    )
    parser.add_argument(
        "--root-path", type=str, default=".", help="Root path for the application"
    )
    parser.add_argument(
        "--limit-concurrency", type=int, help="Max concurrent requests allowed"
    )
    parser.add_argument("--backlog", type=int, default=2048, help="Max backlog size")
    parser.add_argument(
        "--limit-max-requests", type=int, default=256, help="Max requests limit"
    )
    parser.add_argument(
        "--timeout-keep-alive", type=int, default=5, help="Keep-alive timeout"
    )

    # SSL options parser.add_argument("--ssl-keyfile", type=str,
    # default="/usr/local/app/.certs/delliusalexander.key", help="Path to SSL keyfile") parser.add_argument(
    # "--ssl-certfile", type=str, default="/usr/local/app/.certs/delliusalexander.crt", help="Path to SSL certfile")
    # parser.add_argument("--ssl-keyfile-password", type=str, default=None, help="Password for SSL keyfile")
    # parser.add_argument("--ssl-version", type=int, default=3, help="SSL protocol version to use")
    # parser.add_argument("--ssl-cert-reqs", type=int, default=ssl.CERT_NONE, help="SSL cert requirements")
    # parser.add_argument("--ssl-ca-certs", type=str, default="/usr/local/app/.certs/delliusalexander.pem",
    # help="Path to SSL CA certs file") parser.add_argument("--ssl-ciphers", type=str, default="TLSv1",
    # help="SSL ciphers to use")

    # Miscellaneous options
    parser.add_argument(
        "--headers", type=list, default=[], help="Additional headers to send"
    )
    parser.add_argument(
        "--use-colors",
        type=bool,
        default=True,
        help="Enable/disable colors in console output",
    )
    parser.add_argument(
        "--app-dir",
        type=str,
        default=os.path.dirname(__file__),
        help="Path to the application directory",
    )
    parser.add_argument(
        "--factory", type=bool, default=False, help="Enable/disable factory mode"
    )
    parser.add_argument(
        "--h11-max-incomplete-event-size",
        type=int,
        default=8192,
        help="Max size of incomplete H11 events",
    )
    return parser


# -----------------------------------------------------------------------------
# Main entry point
if __name__ == "__main__":
    # Parse the command line
    # parser = get_parser()
    # args = parser.parse_args()
    try:
        # Start the application
        uvicorn.run(
            app="main:app",
            host="0.0.0.0",
            port=8000,
            loop="auto",
            # log_level="debug",
            reload=True,
            use_colors=True,
            proxy_headers=True,
        )
    except Exception as e:
        print("Error: uvicorn module not found.")
        print(e)
        print(traceback.format_exc())
