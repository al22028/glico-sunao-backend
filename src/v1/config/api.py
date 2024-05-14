# Standard Library
import os

STAGE = os.environ.get("STAGE", "local")

API_VERSION_HASH = os.environ.get("API_VERSION_HASH", "latest")

APP_API_CORS_ALLOWED_ORIGINS = os.environ.get(
    "APP_API_CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:3005",
).split(",")
