import asyncio
import time
from typing import Any

import httpx
from loguru import logger

from lotr_sdk.core.errors import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    RetryError,
    ServerError,
)
from lotr_sdk.core.settings import Settings
from lotr_sdk.schemas.base import APIResponse


class HTTPXClient:
    """HTTP client implementation using httpx with retry and error handling."""

    def __init__(self, settings: Settings):
        """Initialize the HTTP client.

        Args:
            settings: Client settings
        """
        self.settings = settings
        self.client = httpx.Client(
            base_url=settings.base_url,
            timeout=settings.timeout,
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "User-Agent": settings.user_agent,
            },
        )
        self.async_client = httpx.AsyncClient(
            base_url=settings.base_url,
            timeout=settings.timeout,
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "User-Agent": settings.user_agent,
            },
        )

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle HTTP errors and convert them to API errors.

        Args:
            response: HTTPX response object

        Raises:
            APIError: Appropriate error based on status code
        """
        if response.status_code == httpx.codes.UNAUTHORIZED:
            raise AuthenticationError()
        elif response.status_code == httpx.codes.NOT_FOUND:
            raise ResourceNotFoundError()
        elif response.status_code == httpx.codes.TOO_MANY_REQUESTS:
            raise RateLimitError()
        elif response.status_code >= httpx.codes.INTERNAL_SERVER_ERROR:
            raise ServerError()
        else:
            raise APIError()

    def _should_retry(self, error: Exception) -> bool:
        """Check if the request should be retried.

        Args:
            error: The error that occurred

        Returns:
            True if the request should be retried, False otherwise
        """
        if isinstance(error, httpx.NetworkError | httpx.TimeoutException | RateLimitError | ServerError):
            return True
        if isinstance(error, httpx.HTTPStatusError):
            return error.response.status_code >= 500
        if isinstance(error, (RateLimitError, ServerError)):
            return True
        return False

    def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> APIResponse[Any]:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            params: Query parameters
            data: Request body data
            headers: Additional request headers

        Returns:
            APIResponse containing the response data

        Raises:
            AuthenticationError: If authentication fails
            ResourceNotFoundError: If resource is not found
            RateLimitError: If rate limit is exceeded
            ServerError: If server returns an error
            RetryError: If all retry attempts are exhausted
        """
        last_error = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                logger.info(
                    "Requesting {method} {url}",
                    method=method,
                    url=url,
                    params=params,
                )
                response = self.client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
                )
                response.raise_for_status()

                return APIResponse(
                    data=response.json(),
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
            except httpx.HTTPStatusError as e:
                last_error = e
                if not self._should_retry(e) or attempt == self.settings.max_retries:
                    self._handle_error(e.response)
                time.sleep(self.settings.retry_delay * (attempt + 1))
            except Exception as e:
                last_error = e
                if not self._should_retry(e) or attempt == self.settings.max_retries:
                    raise APIError()
                time.sleep(self.settings.retry_delay * (attempt + 1))

        raise RetryError()

    async def request_async(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> APIResponse[Any]:
        """Make an HTTP request asynchronously with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            params: Query parameters
            data: Request body data
            headers: Additional request headers

        Returns:
            APIResponse containing the response data

        Raises:
            AuthenticationError: If authentication fails
            ResourceNotFoundError: If resource is not found
            RateLimitError: If rate limit is exceeded
            ServerError: If server returns an error
            RetryError: If all retry attempts are exhausted
        """
        last_error = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                logger.info(
                    "Requesting {method} {url}",
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                )
                response = await self.async_client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
                )
                response.raise_for_status()
                return APIResponse(
                    data=response.json(),
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
            except httpx.HTTPStatusError as e:
                last_error = e
                if not self._should_retry(e) or attempt == self.settings.max_retries:
                    self._handle_error(e.response)
                await asyncio.sleep(self.settings.retry_delay * (attempt + 1))
            except Exception as e:
                last_error = e
                if not self._should_retry(e) or attempt == self.settings.max_retries:
                    raise APIError()
                await asyncio.sleep(self.settings.retry_delay * (attempt + 1))

        raise RetryError()

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    async def close_async(self):
        """Close the HTTP client asynchronously."""
        await self.async_client.aclose()
