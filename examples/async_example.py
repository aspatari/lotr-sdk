import asyncio
import re
import time

from lotr_sdk.core.settings import Settings
from lotr_sdk.lotr import LotrAPI
from lotr_sdk.schemas.base import Pagination


def count_numeric_quotes(quote_dialog):
    """Count the number of quotes containing numeric characters."""
    return bool(re.search(r"\d", quote_dialog))


async def main():
    # Record start time
    start_time = time.time()

    # Initialize the SDK with your API key
    settings = Settings(api_key="YOUR_API_KEY")  # Replace with your API key from The One API
    client = LotrAPI(settings=settings)

    print("🧙 Lord of the Rings SDK - Asynchronous Example")
    print("-----------------------------------------------")

    # Get all movies
    print("Fetching all movies...")
    movies = await client.movies.list_async()
    print(f"Found {len(movies.docs)} movies")

    # Process each movie's quotes concurrently
    numeric_quotes_by_movie = {}
    total_quotes_by_movie = {}
    total_quotes = 0

    async def process_movie(movie):
        nonlocal total_quotes
        print(f"\nProcessing movie: {movie.name}")

        # Get quotes for this movie
        quotes = await client.movies.get_quotes_async(movie.id, pagination=Pagination(limit=1000))

        # Count quotes with numbers
        numeric_quotes = [q for q in quotes.docs if count_numeric_quotes(q.dialog)]
        numeric_quotes_by_movie[movie.name] = len(numeric_quotes)
        total_quotes_by_movie[movie.name] = len(quotes.docs)

        print(f"  - Total quotes: {len(quotes.docs)}")
        print(f"  - Quotes containing numbers: {len(numeric_quotes)}")

        total_quotes += len(quotes.docs)

    # Create tasks for processing all movies concurrently
    tasks = [process_movie(movie) for movie in movies.docs]
    await asyncio.gather(*tasks)

    # Print summary statistics
    print("\n📊 SUMMARY STATISTICS")
    print("--------------------")
    print(f"Total movies: {len(movies.docs)}")
    print(f"Total quotes: {total_quotes}")

    # Sort movies by number of numeric quotes (descending)
    sorted_movies = sorted(numeric_quotes_by_movie.items(), key=lambda x: x[1], reverse=True)

    print("\n🔢 MOVIES BY NUMERIC QUOTES (DESCENDING)")
    print("---------------------------------------")
    for movie_name, count in sorted_movies:
        total = total_quotes_by_movie.get(movie_name, 0)
        if total > 0:
            percent = (count / total) * 100
            print(f"{movie_name}: {count} numeric quotes ({percent:.1f}%)")
        else:
            print(f"{movie_name}: {count} numeric quotes (0.0%)")

    # Record end time and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
