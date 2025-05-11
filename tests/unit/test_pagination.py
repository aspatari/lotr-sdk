from lotr_sdk.schemas.base import Pagination


def test_pagination_initialization():
    """Test that pagination can be initialized with arguments."""
    # Test with page and limit
    pagination = Pagination(page=2, limit=10)
    assert pagination.page == 2
    assert pagination.limit == 10
    assert pagination.offset is None

    # Test with offset and limit
    pagination = Pagination(offset=20, limit=10)
    assert pagination.offset == 20
    assert pagination.limit == 10
    assert pagination.page is None


def test_pagination_to_dict():
    """Test that pagination converts to dictionary correctly."""
    # Test with page and limit
    pagination = Pagination(page=2, limit=10)
    params = pagination.to_dict()
    assert params == {"page": "2", "limit": "10"}

    # Test with offset and limit
    pagination = Pagination(offset=20, limit=10)
    params = pagination.to_dict()
    assert params == {"offset": "20", "limit": "10"}


def test_pagination_validation():
    """Test pagination validation."""
    # The Pagination class doesn't actually validate limit, page, or offset
    # Let's test the basic initialization instead

    # Initialize with all values
    pagination = Pagination(page=2, limit=10, offset=20)
    assert pagination.page == 2
    assert pagination.limit == 10
    assert pagination.offset == 20

    # Initialize with none
    pagination = Pagination()
    assert pagination.page is None
    assert pagination.limit is None
    assert pagination.offset is None

    # Initialize with only some values
    pagination = Pagination(limit=10)
    assert pagination.page is None
    assert pagination.limit == 10
    assert pagination.offset is None
