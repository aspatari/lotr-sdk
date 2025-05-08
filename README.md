# Lord of the Rings SDK

A Python SDK for accessing [The One API](https://the-one-api.dev/) - a comprehensive Lord of the Rings API with data from the quotes and movies.

## Features

- Modern API client for Python 3.13+
- Both synchronous and asynchronous interfaces
- Type hints throughout for excellent IDE integration
- Comprehensive error handling and retries
- Access to movie and quote endpoints
- Pagination support for listing resources
- Advanced filtering capabilities

## Installation

This package is designed to be used with modern Python package managers. We recommend using [UV](https://github.com/astral-sh/uv) for the best performance:

```bash
# Using UV (recommended)
uv pip install lotr-sdk

# Using pip
pip install lotr-sdk
```

## Quickstart

### Async Example

```python
import asyncio
from lotr_sdk import LotrAPI, Settings

async def main():
    # Initialize the SDK with your API key
    settings = Settings(api_key="your-api-key-here")
    lotr = LotrAPI(settings=settings)
    
    # Get all movies
    movies = await lotr.movies.list_async()
    for movie in movies.docs:
        print(f"{movie.name}: {movie.runtime_in_minutes} minutes")
    
    # Get a specific movie by ID
    movie = await lotr.movies.get_async("5cd95395de30eff6ebccde5c")
    print(f"Movie: {movie.name}")
    
    # Get quotes from a movie
    quotes = await lotr.movies.get_quotes_async("5cd95395de30eff6ebccde5c")
    for quote in quotes.docs:
        print(f"Quote: {quote.dialog}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Sync Example

```python
from lotr_sdk import LotrAPI, Settings

# Initialize the SDK with your API key
settings = Settings(api_key="your-api-key-here")
lotr = LotrAPI(settings=settings)

# Get all movies
movies = lotr.movies.list()
for movie in movies.docs:
    print(f"{movie.name}: {movie.runtime_in_minutes} minutes")

# Get a specific movie by ID
movie = lotr.movies.get("5cd95395de30eff6ebccde5c")
print(f"Movie: {movie.name}")

# Get quotes from a movie
quotes = lotr.movies.get_quotes("5cd95395de30eff6ebccde5c")
for quote in quotes.docs:
    print(f"Quote: {quote.dialog}")
```

## Configuration

The SDK is configured using a `Settings` object:

```python
from lotr_sdk import Settings

settings = Settings(
    api_key="your-api-key-here",           # Required
    base_url="https://the-one-api.dev",    # Default
    timeout=30.0,                          # Default
    max_retries=3,                         # Default
    retry_delay=1.0,                       # Default
    user_agent="lotr-sdk/1.0.0"            # Default
)
```

### Environment Variables

You can also configure the SDK using environment variables:

```bash
export LOTR_API_KEY=your-api-key-here
export LOTR_TIMEOUT=60.0
export LOTR_MAX_RETRIES=5
export LOTR_RETRY_DELAY=2.0
export LOTR_BASE_URL=https://the-one-api.dev
export LOTR_USER_AGENT=my-custom-app/1.0
```

## API Reference

### Movies

```python
# Async
# List all movies (with pagination)
movies = await lotr.movies.list_async(pagination=Pagination(page=1, limit=10))

# Get a specific movie by ID
movie = await lotr.movies.get_async("5cd95395de30eff6ebccde5c")

# Get quotes from a movie
quotes = await lotr.movies.get_quotes_async("5cd95395de30eff6ebccde5c", pagination=Pagination(limit=20))

# Sync
# List all movies (with pagination)
movies = lotr.movies.list(pagination=Pagination(page=1, limit=10))

# Get a specific movie by ID
movie = lotr.movies.get("5cd95395de30eff6ebccde5c")

# Get quotes from a movie
quotes = lotr.movies.get_quotes("5cd95395de30eff6ebccde5c", pagination=Pagination(limit=20))
```

#### Movie Data Model

```python
class Movie:
    id: str                              # Unique identifier
    name: str                            # Name of the movie
    runtime_in_minutes: int              # Runtime in minutes
    budget_in_millions: float            # Budget in millions
    box_office_revenue_in_millions: float  # Box office revenue 
    academy_award_nominations: int       # Academy Award nominations
    academy_award_wins: int              # Academy Award wins
    rotten_tomatoes_score: float         # Rotten Tomatoes score
```

### Quotes

```python
# Async
# List all quotes (with pagination)
quotes = await lotr.quotes.list_async(pagination=Pagination(page=1, limit=10))

# Get a specific quote by ID
quote = await lotr.quotes.get_async("5cd96e05de30eff6ebcce7e9")

# Sync
# List all quotes (with pagination)
quotes = lotr.quotes.list(pagination=Pagination(page=1, limit=10))

# Get a specific quote by ID
quote = lotr.quotes.get("5cd96e05de30eff6ebcce7e9")
```

## Pagination

List operations return paginated results. You can control pagination using the `Pagination` object:

```python
from lotr_sdk.schemas.base import Pagination

# Async example
# Get the first page with 10 items per page
page1 = await lotr.movies.list_async(pagination=Pagination(page=1, limit=10))
print(f"Page 1: {len(page1.docs)} movies")

# Get the second page
page2 = await lotr.movies.list_async(pagination=Pagination(page=2, limit=10))
print(f"Page 2: {len(page2.docs)} movies")

# Use offset instead of page
offset_results = await lotr.movies.list_async(pagination=Pagination(offset=5, limit=5))
print(f"Offset results: {len(offset_results.docs)} movies")

# Sync example
# Get the first page with 5 items per page
page1 = lotr.movies.list(pagination=Pagination(page=1, limit=5))
print(f"Showing page {page1.page} of {page1.pages} (Total items: {page1.total})")

# Iterate through all pages
current_page = 1
total_pages = page1.pages
while current_page <= total_pages:
    result = lotr.movies.list(pagination=Pagination(page=current_page, limit=5))
    print(f"Page {current_page}: {len(result.docs)} items")
    for item in result.docs:
        print(f"- {item.name}")
    current_page += 1
```

Pagination response structure:

```python
result = await lotr.movies.list_async()

print(f"Total records: {result.total}")
print(f"Pages: {result.pages}")
print(f"Current page: {result.page}")
print(f"Limit per page: {result.limit}")
print(f"Offset: {result.offset}")

# Access the actual data
for item in result.docs:
    print(item)
```

## Filtering

The SDK supports advanced filtering capabilities to narrow down query results:

### Basic Filtering Examples

```python
from lotr_sdk.schemas.base import FieldFilter
from lotr_sdk.schemas.movie import MovieFilters
from lotr_sdk.schemas.base import Pagination

# Async example - Find movies with runtime greater than 200 minutes
filters = MovieFilters(
    runtime_in_minutes=FieldFilter(gt=200)
)
long_movies = await lotr.movies.list_async(filters=filters)
print(f"Found {len(long_movies.docs)} long movies")

# Sync example - Find movies with high rating
filters = MovieFilters(
    rotten_tomatoes_score=FieldFilter(gte=90)
)
top_rated = lotr.movies.list(filters=filters)
for movie in top_rated.docs:
    print(f"{movie.name}: {movie.rotten_tomatoes_score}% on Rotten Tomatoes")

# Combining filtering with pagination
filters = MovieFilters(
    budget_in_millions=FieldFilter(gt=100)
)
pagination = Pagination(page=1, limit=5)
expensive_movies = lotr.movies.list(filters=filters, pagination=pagination)
```

### Advanced Filtering Examples

```python
# Find movies with Academy Award wins between 5 and 15
filters = MovieFilters(
    academy_award_wins=FieldFilter(gte=5, lte=15)
)

# Find movies with specific name
filters = MovieFilters(
    name=FieldFilter(match="The Fellowship of the Ring")
)

# Exclude specific movies
filters = MovieFilters(
    name=FieldFilter(exclude=["The Hobbit"])
)

# Find movies with budget greater than 100 million AND rating over 85%
filters = MovieFilters(
    budget_in_millions=FieldFilter(gt=100),
    rotten_tomatoes_score=FieldFilter(gt=85)
)

# Use a regex to find movies
filters = MovieFilters(
    name=FieldFilter(regex="^The")  # Names starting with "The"
)

# Combined example (sync) with pagination
filters = MovieFilters(
    runtime_in_minutes=FieldFilter(lt=200),
    academy_award_wins=FieldFilter(gt=0),
    rotten_tomatoes_score=FieldFilter(gt=80)
)
pagination = Pagination(page=1, limit=5)
movies = lotr.movies.list(filters=filters, pagination=pagination)
```

Available filter operations:
- `match`: Exact match for the value
- `not_match`: Not equal to the value
- `include`: Value must be in the provided list
- `exclude`: Value must not be in the provided list
- `exists`: Field must exist (True) or not exist (False)
- `regex`: Match against a regular expression
- `gt`, `gte`, `lt`, `lte`: Greater than, greater than or equal, less than, less than or equal

## Error Handling

The SDK provides proper error handling with specific exceptions:

```python
from lotr_sdk.core.errors import APIError, AuthenticationError, ResourceNotFoundError

try:
    movies = await lotr.movies.list_async()
except AuthenticationError:
    print("Invalid API key")
except ResourceNotFoundError:
    print("The requested resource was not found")
except APIError as e:
    print(f"API error: {e}")
```

Available exceptions:
- `APIError`: Base exception for all API errors
- `AuthenticationError`: Raised when authentication fails
- `ValidationError`: Raised when request validation fails
- `ResourceNotFoundError`: Raised when a requested resource is not found
- `RateLimitError`: Raised when rate limit is exceeded
- `ServerError`: Raised when server returns an error
- `RetryError`: Raised when all retry attempts are exhausted

## Development

### Requirements

- Python 3.13+
- UV (recommended for dependency management)

### Setup

```bash
# Clone the repository
git clone https://github.com/aspatari/lotr-sdk.git
cd lotr-sdk

# Create a virtual environment and install dependencies with UV
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

MIT
