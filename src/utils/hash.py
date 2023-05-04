import bcrypt

# Get the logger
from myLogger.Logger import getLogger as GetLogger

log = GetLogger(__name__)


# -----------------------------------------------------------------------------
# Hash a password
def hash_password(password):
    """
    Hash a password for storing.

    :param password: The password to hash.
    :return: A string containing the hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    log.info("Hashed password: %s" % hashed_password.decode("utf-8"))
    return hashed_password.decode("utf-8")
