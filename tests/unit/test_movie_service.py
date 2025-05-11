import pytest

from lotr_sdk.core.errors import ResourceNotFoundError
from lotr_sdk.schemas.base import FieldFilter, Pagination
from lotr_sdk.schemas.movie import Movie, MovieFilters, MovieList
from lotr_sdk.schemas.quote import QuoteList
from lotr_sdk.services.movie import MovieService


@pytest.fixture
def movie_service(mock_http_client):
    """Fixture for MovieService with mock HTTP client."""
    return MovieService(mock_http_client)


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


@pytest.fixture
def sample_quotes_data():
    """Sample quotes data for testing."""
    return {
        "docs": [
            {
                "id": "5cd96e05de30eff6ebcce7e9",
                "dialog": "Deagol!",
                "movie": "5cd95395de30eff6ebccde5d",
                "character": "5cd99d4bde30eff6ebccfe9e",
            }
        ],
        "total": 1,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1,
    }


def test_list_movies(movie_service, mock_http_client, sample_movie_data):
    """Test listing movies."""
    # Configure mock response
    mock_http_client.configure_response(sample_movie_data)

    # Call list method
    result = movie_service.list()

    # Verify HTTP client was called correctly
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url="/v2/movie",
        params={},
    )

    # Check result is correct type
    assert isinstance(result, MovieList)  # type: ignore
    assert len(result.docs) == 1
    assert isinstance(result.docs[0], Movie)
    assert result.docs[0].name == "The Fellowship of the Ring"


def test_list_movies_with_filters(movie_service, mock_http_client, sample_movie_data):
    """Test listing movies with filters."""
    # Configure mock response
    mock_http_client.configure_response(sample_movie_data)

    # Set up filters
    filters = MovieFilters(runtime_in_minutes=FieldFilter(gt=150))

    # Call list method with filters
    result = movie_service.list(filters=filters)

    # Verify HTTP client was called with correct parameters
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url="/v2/movie",
        params={"runtimeInMinutes>": 150},
    )


def test_list_movies_with_pagination(movie_service, mock_http_client, sample_movie_data):
    """Test listing movies with pagination."""
    # Configure mock response
    mock_http_client.configure_response(sample_movie_data)

    # Set up pagination
    pagination = Pagination(page=2, limit=10)

    # Call list method with pagination
    result = movie_service.list(pagination=pagination)

    # Verify HTTP client was called with correct parameters
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url="/v2/movie",
        params={"page": "2", "limit": "10"},
    )


def test_get_movie(movie_service, mock_http_client, sample_movie_data):
    """Test getting a specific movie by ID."""
    # Configure mock response
    mock_http_client.configure_response(sample_movie_data)

    # Call get method
    movie_id = "5cd95395de30eff6ebccde5c"
    result = movie_service.get(movie_id)

    # Verify HTTP client was called correctly
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url=f"/v2/movie/{movie_id}",
    )

    # Check result is correct type
    assert isinstance(result, Movie)
    assert result.id == movie_id
    assert result.name == "The Fellowship of the Ring"


def test_get_movie_not_found(movie_service, mock_http_client):
    """Test getting a movie that doesn't exist."""
    # Configure mock response with no docs
    mock_http_client.configure_response({"docs": []})

    # Call get method and expect exception
    movie_id = "non-existent-id"
    with pytest.raises(ResourceNotFoundError):
        movie_service.get(movie_id)


def test_get_quotes(movie_service, mock_http_client, sample_quotes_data):
    """Test getting quotes for a movie."""
    # Configure mock response
    mock_http_client.configure_response(sample_quotes_data)

    # Call get_quotes method
    movie_id = "5cd95395de30eff6ebccde5d"
    result = movie_service.get_quotes(movie_id)

    # Verify HTTP client was called correctly
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url=f"/v2/movie/{movie_id}/quote",
        params={},
    )

    # Check result is correct type
    assert isinstance(result, QuoteList)
    assert len(result.docs) == 1
    assert result.docs[0].dialog == "Deagol!"


@pytest.mark.asyncio
async def test_list_movies_async(movie_service, mock_http_client, sample_movie_data):
    """Test listing movies asynchronously."""
    # Configure mock response
    mock_http_client.configure_response(sample_movie_data)

    # Call list_async method
    result = await movie_service.list_async()

    # Verify HTTP client was called correctly
    mock_http_client.request_async.assert_called_once_with(
        method="GET",
        url="/v2/movie",
        params={},
    )

    # Check result is correct type
    assert isinstance(result, MovieList)  # type: ignore
    assert len(result.docs) == 1
    assert result.docs[0].name == "The Fellowship of the Ring"


@pytest.mark.asyncio
async def test_get_movie_async(movie_service, mock_http_client, sample_movie_data):
    """Test getting a specific movie by ID asynchronously."""
    # Configure mock response
    mock_http_client.configure_response(sample_movie_data)

    # Call get_async method
    movie_id = "5cd95395de30eff6ebccde5c"
    result = await movie_service.get_async(movie_id)

    # Verify HTTP client was called correctly
    mock_http_client.request_async.assert_called_once_with(
        method="GET",
        url=f"/v2/movie/{movie_id}",
    )

    # Check result is correct type
    assert isinstance(result, Movie)
    assert result.id == movie_id


@pytest.mark.asyncio
async def test_get_quotes_async(movie_service, mock_http_client, sample_quotes_data):
    """Test getting quotes for a movie asynchronously."""
    # Configure mock response
    mock_http_client.configure_response(sample_quotes_data)

    # Call get_quotes_async method
    movie_id = "5cd95395de30eff6ebccde5d"
    result = await movie_service.get_quotes_async(movie_id)

    # Verify HTTP client was called correctly
    mock_http_client.request_async.assert_called_once_with(
        method="GET",
        url=f"/v2/movie/{movie_id}/quote",
        params={},
    )

    # Check result is correct type
    assert isinstance(result, QuoteList)
    assert len(result.docs) == 1
