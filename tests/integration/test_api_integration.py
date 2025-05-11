import pytest
from pytest_httpx import HTTPXMock

from lotr_sdk import LotrAPI, Settings
from lotr_sdk.schemas.movie import Movie


@pytest.fixture
def lotr_api():
    """Fixture for LotrAPI with test settings."""
    settings = Settings(api_key="test-api-key")
    return LotrAPI(settings=settings)


@pytest.fixture
def sample_movie_data():
    """Sample movie data for testing."""
    return {
        "docs": [
            {
                "id": "5cd95395de30eff6ebccde5c",
                "name": "The Fellowship of the Ring",
                "runtime_in_minutes": 178,
                "budget_in_millions": 93,
                "box_office_revenue_in_millions": 871.5,
                "academy_award_nominations": 13,
                "academy_award_wins": 4,
                "rotten_tomatoes_score": 91,
            }
        ],
        "total": 1,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1,
    }


def test_list_movies(lotr_api, httpx_mock: HTTPXMock, sample_movie_data):
    """Test the list_movies method with mocked HTTP responses."""
    # Configure mock to return the sample data for GET requests to the movie endpoint
    httpx_mock.add_response(
        method="GET",
        url="https://the-one-api.dev/v2/movie",
        json=sample_movie_data,
        status_code=200,
    )

    # Call the method being tested
    result = lotr_api.movies.list()

    # Verify expected behavior
    assert len(result.docs) == 1
    assert result.docs[0].name == "The Fellowship of the Ring"
    assert result.total == 1


def test_get_movie(lotr_api, httpx_mock: HTTPXMock, sample_movie_data):
    """Test the get_movie method with mocked HTTP responses."""
    movie_id = "5cd95395de30eff6ebccde5c"

    # Configure mock to return the sample data for GET requests to the movie endpoint
    httpx_mock.add_response(
        method="GET",
        url=f"https://the-one-api.dev/v2/movie/{movie_id}",
        json=sample_movie_data,
        status_code=200,
    )

    # Call the method being tested
    movie = lotr_api.movies.get(movie_id)

    # Verify expected behavior
    assert isinstance(movie, Movie)
    assert movie.id == movie_id
    assert movie.name == "The Fellowship of the Ring"


@pytest.mark.asyncio
async def test_list_movies_async(lotr_api, httpx_mock: HTTPXMock, sample_movie_data):
    """Test the list_movies_async method with mocked HTTP responses."""
    # Configure mock to return the sample data for GET requests to the movie endpoint
    httpx_mock.add_response(
        method="GET",
        url="https://the-one-api.dev/v2/movie",
        json=sample_movie_data,
        status_code=200,
    )

    # Call the async method being tested
    result = await lotr_api.movies.list_async()

    # Verify expected behavior
    assert len(result.docs) == 1
    assert result.docs[0].name == "The Fellowship of the Ring"
    assert result.total == 1


def test_authentication_header(lotr_api, httpx_mock: HTTPXMock, sample_movie_data):
    """Test that the API key is sent in the authentication header."""
    # Add a response and capture the request for inspection
    httpx_mock.add_response(
        method="GET",
        url="https://the-one-api.dev/v2/movie",
        json=sample_movie_data,
        status_code=200,
        match_headers={"Authorization": "Bearer test-api-key"},
    )

    # Call the method that should send the auth header
    result = lotr_api.movies.list()

    # The test will fail if the header doesn't match what we specified in match_headers
    assert len(result.docs) == 1
