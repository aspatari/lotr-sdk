class APIError(Exception):
    """Base exception for all API errors."""


class AuthenticationError(APIError):
    """Raised when authentication fails."""


class ValidationError(APIError):
    """Raised when request validation fails."""


class ResourceNotFoundError(APIError):
    """Raised when a requested resource is not found."""


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""


class ServerError(APIError):
    """Raised when server returns an error."""


class RetryError(APIError):
    """Raised when all retry attempts are exhausted."""
