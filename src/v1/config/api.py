# Standard Library
import os

STAGE = os.environ.get("STAGE", "local")

APP_API_VERSION = os.environ.get("APP_API_VERSION", "v1")
APP_COMMIT_HASH = os.environ.get("APP_COMMIT_HASH", "unknown")
