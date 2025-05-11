import pytest

from lotr_sdk.core.errors import ResourceNotFoundError
from lotr_sdk.schemas.base import FieldFilter, Pagination
from lotr_sdk.schemas.quote import Quote, QuoteFilters, QuoteList
from lotr_sdk.services.quote import QuoteService


@pytest.fixture
def quote_service(mock_http_client):
    """Fixture for QuoteService with mock HTTP client."""
    return QuoteService(mock_http_client)


@pytest.fixture
def sample_quote_data():
    """Sample quote data for testing."""
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


def test_list_quotes(quote_service, mock_http_client, sample_quote_data):
    """Test listing quotes."""
    # Configure mock response
    mock_http_client.configure_response(sample_quote_data)

    # Call list method
    result = quote_service.list()

    # Verify HTTP client was called correctly
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url="/v2/quote",
        params={},
    )

    # Check result is correct type
    assert isinstance(result, QuoteList)
    assert len(result.docs) == 1
    assert isinstance(result.docs[0], Quote)
    assert result.docs[0].dialog == "Deagol!"


def test_list_quotes_with_filters(quote_service, mock_http_client, sample_quote_data):
    """Test listing quotes with filters."""
    # Configure mock response
    mock_http_client.configure_response(sample_quote_data)

    # Set up filters
    filters = QuoteFilters(dialog=FieldFilter(match="Deagol!"))

    # Call list method with filters
    result = quote_service.list(filters=filters)

    # Verify HTTP client was called with correct parameters
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url="/v2/quote",
        params={"dialog": "Deagol!"},
    )


def test_list_quotes_with_pagination(quote_service, mock_http_client, sample_quote_data):
    """Test listing quotes with pagination."""
    # Configure mock response
    mock_http_client.configure_response(sample_quote_data)

    # Set up pagination
    pagination = Pagination(page=2, limit=10)

    # Call list method with pagination
    result = quote_service.list(pagination=pagination)

    # Verify HTTP client was called with correct parameters
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url="/v2/quote",
        params={"page": "2", "limit": "10"},
    )


def test_get_quote(quote_service, mock_http_client, sample_quote_data):
    """Test getting a specific quote by ID."""
    # Configure mock response
    mock_http_client.configure_response(sample_quote_data)

    # Call get method
    quote_id = "5cd96e05de30eff6ebcce7e9"
    result = quote_service.get(quote_id)

    # Verify HTTP client was called correctly
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url=f"/v2/quote/{quote_id}",
    )

    # Check result is correct type
    assert isinstance(result, Quote)
    assert result.id == quote_id
    assert result.dialog == "Deagol!"


def test_get_quote_not_found(quote_service, mock_http_client):
    """Test getting a quote that doesn't exist."""
    # Configure mock response with no docs
    mock_http_client.configure_response({"docs": []})

    # Call get method and expect exception
    quote_id = "non-existent-id"
    with pytest.raises(ResourceNotFoundError):
        quote_service.get(quote_id)


@pytest.mark.asyncio
async def test_list_quotes_async(quote_service, mock_http_client, sample_quote_data):
    """Test listing quotes asynchronously."""
    # Configure mock response
    mock_http_client.configure_response(sample_quote_data)

    # Call list_async method
    result = await quote_service.list_async()

    # Verify HTTP client was called correctly
    mock_http_client.request_async.assert_called_once_with(
        method="GET",
        url="/v2/quote",
        params={},
    )

    # Check result is correct type
    assert isinstance(result, QuoteList)
    assert len(result.docs) == 1
    assert result.docs[0].dialog == "Deagol!"


@pytest.mark.asyncio
async def test_get_quote_async(quote_service, mock_http_client, sample_quote_data):
    """Test getting a specific quote by ID asynchronously."""
    # Configure mock response
    mock_http_client.configure_response(sample_quote_data)

    # Call get_async method
    quote_id = "5cd96e05de30eff6ebcce7e9"
    result = await quote_service.get_async(quote_id)

    # Verify HTTP client was called correctly
    mock_http_client.request_async.assert_called_once_with(
        method="GET",
        url=f"/v2/quote/{quote_id}",
    )

    # Check result is correct type
    assert isinstance(result, Quote)
    assert result.id == quote_id
    assert result.dialog == "Deagol!"
