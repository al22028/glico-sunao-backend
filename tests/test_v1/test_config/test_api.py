# Third Party Library
from config import api


def test_stage() -> None:
    assert api.STAGE is not None
    assert api.STAGE == "local"
    assert isinstance(api.STAGE, str)


def test_api_version_hash() -> None:
    assert api.API_VERSION_HASH is not None
    assert api.API_VERSION_HASH == "latest"
    assert isinstance(api.API_VERSION_HASH, str)


def test_app_api_cors_allowed_origins() -> None:
    assert api.APP_API_CORS_ALLOWED_ORIGINS is not None
    assert isinstance(api.APP_API_CORS_ALLOWED_ORIGINS, list)
    assert api.APP_API_CORS_ALLOWED_ORIGINS == ["http://localhost:3000", "http://localhost:3005"]
    assert "http://localhost:3005" in api.APP_API_CORS_ALLOWED_ORIGINS
    assert "http://localhost:3000" in api.APP_API_CORS_ALLOWED_ORIGINS
