import pytest

from lotr_sdk import LotrAPI, Settings
from lotr_sdk.schemas.base import Pagination


@pytest.fixture
def lotr_api():
    """Fixture for LotrAPI with a real API key."""
    settings = Settings(api_key="qQg8z34W2l1bV1I1jGr_")
    return LotrAPI(settings=settings)


@pytest.mark.real_api
def test_list_movies_real_api(lotr_api):
    """Test listing movies with the real API."""
    # Call list method
    result = lotr_api.movies.list(pagination=Pagination(limit=3))

    # Verify we got results
    assert len(result.docs) > 0
    assert result.total > 0
    assert all(hasattr(movie, "name") for movie in result.docs)

    # Print some info for debugging
    print(f"\nFound {result.total} movies in total")
    for movie in result.docs:
        print(f"- {movie.name} ({movie.runtime_in_minutes} minutes)")


@pytest.mark.real_api
def test_get_movie_real_api(lotr_api):
    """Test getting a specific movie with the real API."""
    # The Fellowship of the Ring ID
    movie_id = "5cd95395de30eff6ebccde5c"

    # Call get method
    movie = lotr_api.movies.get(movie_id)

    # Verify we got the right movie
    assert movie.id == movie_id
    assert movie.name == "The Fellowship of the Ring"
    assert movie.runtime_in_minutes == 178

    # Print some info for debugging
    print(f"\nMovie: {movie.name}")
    print(f"Runtime: {movie.runtime_in_minutes} minutes")
    print(f"Academy Award Wins: {movie.academy_award_wins}")


@pytest.mark.real_api
def test_get_movie_quotes_real_api(lotr_api):
    """Test getting quotes from a movie with the real API."""
    # The Fellowship of the Ring ID
    movie_id = "5cd95395de30eff6ebccde5c"

    # Call get_quotes method
    quotes = lotr_api.movies.get_quotes(movie_id, pagination=Pagination(limit=5))

    # Verify we got quotes
    assert len(quotes.docs) > 0
    assert quotes.total > 0
    assert all(hasattr(quote, "dialog") for quote in quotes.docs)

    # Print some info for debugging
    print(f"\nFound {quotes.total} quotes for this movie")
    for i, quote in enumerate(quotes.docs[:5]):
        print(f'{i + 1}. "{quote.dialog}"')


@pytest.mark.real_api
@pytest.mark.asyncio
async def test_async_api_real_api(lotr_api):
    """Test async methods with the real API."""
    # Call list_async method
    result = await lotr_api.movies.list_async(pagination=Pagination(limit=3))

    # Verify we got results
    assert len(result.docs) > 0
    assert result.total > 0

    # Print some info for debugging
    print(f"\nAsync API test: Found {result.total} movies in total")
    for movie in result.docs:
        print(f"- {movie.name}")
