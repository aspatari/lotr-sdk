import pytest
from pytest_httpx import HTTPXMock

from lotr_sdk import LotrAPI, Settings
from lotr_sdk.core.errors import (
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    ServerError,
)


@pytest.fixture
def lotr_api():
    """Fixture for LotrAPI with test settings."""
    # Use 0 retries to avoid timeouts in tests
    settings = Settings(api_key="test-api-key", max_retries=0)
    return LotrAPI(settings=settings)


def test_authentication_error(lotr_api, httpx_mock: HTTPXMock):
    """Test that authentication errors are handled properly."""
    # Mock a 401 Unauthorized response
    httpx_mock.add_response(
        method="GET",
        url="https://the-one-api.dev/v2/movie",
        json={"message": "Invalid API key"},
        status_code=401,
    )

    # Test that the appropriate exception is raised
    with pytest.raises(AuthenticationError):
        lotr_api.movies.list()


def test_resource_not_found_error(lotr_api, httpx_mock: HTTPXMock):
    """Test that 404 errors are handled properly."""
    movie_id = "non-existent-id"

    # Mock a 404 Not Found response
    httpx_mock.add_response(
        method="GET",
        url=f"https://the-one-api.dev/v2/movie/{movie_id}",
        json={"message": "Not found"},
        status_code=404,
    )

    # Test that the appropriate exception is raised
    with pytest.raises(ResourceNotFoundError):
        lotr_api.movies.get(movie_id)


def test_rate_limit_error(lotr_api, httpx_mock: HTTPXMock):
    """Test that rate limit errors are handled properly."""
    # Mock a 429 Too Many Requests response
    httpx_mock.add_response(
        method="GET",
        url="https://the-one-api.dev/v2/movie",
        json={"message": "Too many requests"},
        status_code=429,
    )

    # Test that the appropriate exception is raised
    with pytest.raises(RateLimitError):
        lotr_api.movies.list()


def test_server_error(lotr_api, httpx_mock: HTTPXMock):
    """Test that server errors are handled properly."""
    # Mock a 500 Internal Server Error response
    httpx_mock.add_response(
        method="GET",
        url="https://the-one-api.dev/v2/movie",
        json={"message": "Internal server error"},
        status_code=500,
    )

    # Test that the appropriate exception is raised
    with pytest.raises(ServerError):
        lotr_api.movies.list()


@pytest.mark.asyncio
async def test_async_error_handling(lotr_api, httpx_mock: HTTPXMock):
    """Test that errors in async methods are handled properly."""
    # Mock a 401 Unauthorized response
    httpx_mock.add_response(
        method="GET",
        url="https://the-one-api.dev/v2/movie",
        json={"message": "Invalid API key"},
        status_code=401,
    )

    # Test that the appropriate exception is raised in the async method
    with pytest.raises(AuthenticationError):
        await lotr_api.movies.list_async()
