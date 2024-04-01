# Third Party Library
from config import api


def test_stage() -> None:
    assert api.STAGE is not None
    assert api.STAGE == "local"


def test_api_version() -> None:
    assert api.APP_API_VERSION is not None
    assert api.APP_API_VERSION == "v1"


def test_commit_hash() -> None:
    assert api.APP_COMMIT_HASH is not None
    assert api.APP_COMMIT_HASH == "unknown"


def test_app_api_cors_allowed_origins() -> None:
    assert api.APP_API_CORS_ALLOWED_ORIGINS is not None
    assert api.APP_API_CORS_ALLOWED_ORIGINS == ["http://localhost:5173"]
