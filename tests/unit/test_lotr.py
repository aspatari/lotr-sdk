from lotr_sdk import LotrAPI
from lotr_sdk.services.movie import MovieService
from lotr_sdk.services.quote import QuoteService


def test_lotr_api_initialization(mock_settings, mock_http_client):
    """Test that LotrAPI initializes correctly with settings and http client."""
    api = LotrAPI(settings=mock_settings, http_client=mock_http_client)

    # Test that settings are set correctly
    assert api.settings == mock_settings

    # Test that the HTTP client is set correctly
    assert api._http_client == mock_http_client

    # Test that services are initialized properly
    assert isinstance(api.movies, MovieService)
    assert isinstance(api.quotes, QuoteService)

    # Test that services use the same HTTP client
    assert api.movies.http_client == mock_http_client
    assert api.quotes.http_client == mock_http_client
