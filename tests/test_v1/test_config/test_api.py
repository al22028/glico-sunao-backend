# Third Party Library
from config import api


def test_stage() -> None:
    assert api.STAGE is not None
    assert api.STAGE == "local"


def test_api_version_hash() -> None:
    assert api.API_VERSION_HASH is not None
    assert api.API_VERSION_HASH == "latest"


def test_app_api_cors_allowed_origins() -> None:
    assert api.APP_API_CORS_ALLOWED_ORIGINS is not None
    assert api.APP_API_CORS_ALLOWED_ORIGINS == ["http://localhost:5173"]
