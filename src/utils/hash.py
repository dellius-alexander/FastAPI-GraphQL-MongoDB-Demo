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


# -----------------------------------------------------------------------------
# Check a password
def check_password(password, hashed_password) -> bool:
    """
    Check a password against an existing hash.

    :param password: The password to check.
    :param hashed_password: The existing hash.
    :return: True if the password matches the hash. False otherwise.
    """
    # Hash the password with the salt
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# -----------------------------------------------------------------------------
