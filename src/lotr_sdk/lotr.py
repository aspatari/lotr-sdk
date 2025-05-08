from lotr_sdk.client.base import HTTPClient
from lotr_sdk.client.httpx import HTTPXClient
from lotr_sdk.core.settings import Settings
from lotr_sdk.services.movie import MovieService
from lotr_sdk.services.quote import QuoteService


class LotrAPI:
    """Main SDK class that provides access to all resources."""

    def __init__(
        self,
        *,
        settings: Settings,
        http_client: HTTPClient | None = None,
    ):
        self.settings = settings
        self._http_client = http_client or HTTPXClient(settings=self.settings)

        self.movies = MovieService(self._http_client)
        self.quotes = QuoteService(self._http_client)
