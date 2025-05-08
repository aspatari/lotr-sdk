from lotr_sdk.client.base import HTTPClient
from lotr_sdk.core.errors import ResourceNotFoundError
from lotr_sdk.schemas.base import Pagination
from lotr_sdk.schemas.quote import Quote, QuoteFilters, QuoteList


class QuoteService:
    """Service for interacting with the Movie API endpoints."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.base_url = "/v2/quote"

    def list(
        self,
        *,
        filters: QuoteFilters | None = None,
        pagination: Pagination | None = None,
    ) -> QuoteList:
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

        return QuoteList(**response.data)

    async def list_async(
        self,
        *,
        filters: QuoteFilters | None = None,
        pagination: Pagination | None = None,
    ) -> QuoteList:
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

        return QuoteList(**response.data)

    def get(self, quote_id: str) -> Quote:
        response = self.http_client.request(
            method="GET",
            url=f"{self.base_url}/{quote_id}",
        )
        docs = response.data.get("docs", [])
        if not docs:
            raise ResourceNotFoundError(f"Quote with id {quote_id} not found")

        return Quote(**docs[0])

    async def get_async(self, quote_id: str) -> Quote:
        response = await self.http_client.request_async(
            method="GET",
            url=f"{self.base_url}/{quote_id}",
        )
        docs = response.data.get("docs", [])
        if not docs:
            raise ResourceNotFoundError(f"Quote with id {quote_id} not found")

        return Quote(**docs[0])
