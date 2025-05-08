from lotr_sdk.client.base import HTTPClient
from lotr_sdk.core.errors import ResourceNotFoundError
from lotr_sdk.schemas.base import Pagination
from lotr_sdk.schemas.movie import Movie, MovieFilters, MovieList
from lotr_sdk.schemas.quote import QuoteList


class MovieService:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_url = "/v2/movie"

    def list(
        self,
        *,
        filters: MovieFilters | None = None,
        pagination: Pagination | None = None,
    ) -> MovieList:
        params: dict[str, str] = {}

        if filters:
            params.update(filters.to_dict())

        if pagination:
            params.update(pagination.to_dict())

        response = self.http_client.request(
            method="GET",
            url=self.base_url,
            params=params,
        )

        return MovieList(**response.data)

    async def list_async(
        self,
        *,
        filters: MovieFilters | None = None,
        pagination: Pagination | None = None,
    ) -> MovieList:
        params: dict[str, str] = {}

        if filters:
            params.update(filters.to_dict())

        if pagination:
            params.update(pagination.to_dict())

        response = await self.http_client.request_async(
            method="GET",
            url=self.base_url,
            params=params,
        )
        return MovieList(**response.data)

    def get(self, movie_id: str) -> Movie:
        response = self.http_client.request(
            method="GET",
            url=f"{self.base_url}/{movie_id}",
        )

        docs = response.data.get("docs")
        if not docs:
            raise ResourceNotFoundError("No docs found in response")

        return Movie(**docs[0])

    async def get_async(self, movie_id: str) -> Movie:
        response = await self.http_client.request_async(
            method="GET",
            url=f"{self.base_url}/{movie_id}",
        )

        docs = response.data.get("docs")
        if not docs:
            raise ResourceNotFoundError("No docs found in response")

        return Movie(**docs[0])

    def get_quotes(
        self,
        movie_id: str,
        *,
        pagination: Pagination | None = None,
    ) -> QuoteList:
        params: dict[str, str] = {}
        if pagination:
            params.update(pagination.to_dict())

        response = self.http_client.request(
            method="GET",
            url=f"{self.base_url}/{movie_id}/quote",
            params=params,
        )

        return QuoteList(**response.data)

    async def get_quotes_async(
        self,
        movie_id: str,
        *,
        pagination: Pagination | None = None,
    ) -> QuoteList:
        params: dict[str, str] = {}
        if pagination:
            params.update(pagination.to_dict())

        response = await self.http_client.request_async(
            method="GET",
            url=f"{self.base_url}/{movie_id}/quote",
            params=params,
        )

        return QuoteList(**response.data)
