from typing import Any, Protocol

from lotr_sdk.core.settings import Settings
from lotr_sdk.schemas.base import APIResponse


class HTTPClient(Protocol):
    """Protocol defining the interface for HTTP clients."""

    settings: Settings

    def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> APIResponse[Any]:
        """Make an HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            params: Query parameters
            data: Request body data

        Returns:
            APIResponse containing the response data
        """
        ...

    async def request_async(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> APIResponse[Any]:
        """Make an HTTP request asynchronously.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            params: Query parameters
            data: Request body data

        Returns:
            APIResponse containing the response data
        """
        ...
