from pymongo import monitoring
from myLogger.Logger import getLogger as GetLogger
from database.db import connect_to_mongo

log = GetLogger(__name__)


# -----------------------------------------------------------------------------
# Define the command logger
class CommandLogger(monitoring.CommandListener):
    def started(self, event):
        log.debug(
            "Command {0.command_name} with request id "
            "{0.request_id} started on server "
            "{0.connection_id}".format(event)
        )

    def succeeded(self, event):
        log.debug(
            "Command {0.command_name} with request id "
            "{0.request_id} on server {0.connection_id} "
            "succeeded in {0.duration_micros} "
            "microseconds".format(event)
        )

    def failed(self, event):
        log.debug(
            "Command {0.command_name} with request id "
            "{0.request_id} on server {0.connection_id} "
            "failed in {0.duration_micros} "
            "microseconds".format(event)
        )


# -----------------------------------------------------------------------------
monitoring.register(CommandLogger())
connect_to_mongo()
# -----------------------------------------------------------------------------
