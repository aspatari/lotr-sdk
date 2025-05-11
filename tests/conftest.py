from unittest.mock import AsyncMock, MagicMock

import pytest

from lotr_sdk.core.settings import Settings
from lotr_sdk.schemas.base import APIResponse


class MockHTTPClient:
    """Mock HTTP client for testing."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.request = MagicMock()
        self.request_async = AsyncMock()

    def configure_response(self, data, status_code=200):
        """Configure mock response for both sync and async methods."""
        response = APIResponse(
            data=data,
            status_code=status_code,
            headers={},
        )
        self.request.return_value = response
        self.request_async.return_value = response


@pytest.fixture
def mock_settings():
    """Fixture for test settings."""
    return Settings(api_key="test-api-key")


@pytest.fixture
def mock_http_client(mock_settings):
    """Fixture for mock HTTP client."""
    return MockHTTPClient(settings=mock_settings)


def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--run-real-api",
        action="store_true",
        default=False,
        help="Run tests that call the real API",
    )


def pytest_collection_modifyitems(config, items):
    """Skip real API tests unless explicitly requested."""
    if not config.getoption("--run-real-api"):
        skip_real_api = pytest.mark.skip(reason="Need --run-real-api option to run")
        for item in items:
            if "real_api" in item.keywords:
                item.add_marker(skip_real_api)
