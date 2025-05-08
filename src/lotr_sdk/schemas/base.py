from dataclasses import dataclass
from typing import Any, Literal, TypeVar

from pydantic import BaseModel, ConfigDict

from lotr_sdk.types import MongoIdField

T = TypeVar("T")


class APIResponse[T](BaseModel):
    """Generic response model for API responses.

    Attributes:
        data: Response data
        status_code: HTTP status code
        headers: Response headers

    """

    data: T
    status_code: int
    headers: dict[str, str]


class PaginatedResponse[T](BaseModel):
    """Generic paginated response from the API.

    Attributes:
        docs: List of items in the current page
        total: Total number of items available
        limit: Number of items per page
        offset: Number of items skipped
        page: Current page number
        pages: Total number of pages
    """

    docs: list[T]
    total: int
    limit: int
    offset: int | None = None
    page: int | None = None
    pages: int | None = None

    model_config = ConfigDict(
        frozen=True,  # Make responses immutable
        strict=True,  # Enforce strict type checking
    )

    def __iter__(self):
        """Return an iterator over the docs."""
        return iter(self.docs)

    def __getitem__(self, index):
        """Get an item from docs by index."""
        return self.docs[index]

    def __len__(self):
        """Return the number of items in docs."""
        return len(self.docs)


class BaseResource(BaseModel):
    """Base model for all resources.

    Attributes:
        id: Unique identifier of the resource
    """

    id: MongoIdField

    model_config = ConfigDict(
        frozen=True,  # Make resources immutable
        strict=True,  # Enforce strict type checking
        populate_by_name=True,  # Allow using both id and _id
    )


@dataclass
class BaseSort:
    """Base class for all sort options."""

    field: str | None = None
    order: Literal["asc", "desc"] = "asc"

    def to_dict(self) -> dict[str, Any]:
        """Convert sort options to dictionary of query parameters."""
        params: dict[str, Any] = {}
        if self.field:
            params["sort"] = f"{self.field}:{self.order or 'asc'}"
        return params


class BaseFilters:
    """Base class for all filters."""

    def to_dict(self) -> dict[str, Any]:
        """Convert filters to dictionary of query parameters."""
        return {}


@dataclass
class Pagination:
    """Pagination parameters for list requests."""

    page: int | None = None
    limit: int | None = None
    offset: int | None = None

    def to_dict(self) -> dict[str, str]:
        """Convert pagination to query parameters."""
        params = {}
        if self.page is not None:
            params["page"] = str(self.page)
        if self.limit is not None:
            params["limit"] = str(self.limit)
        if self.offset is not None:
            params["offset"] = str(self.offset)
        return params


@dataclass
class FieldFilter:
    match: Any = None
    not_match: Any = None
    include: list[Any] | None = None
    exclude: list[Any] | None = None
    exists: bool | None = None
    regex: str | None = None
    gt: Any = None
    gte: Any = None
    lt: Any = None
    lte: Any = None

    def to_dict(self, field: str) -> dict[str, Any]:
        params = {}
        if self.match is not None:
            params[field] = self.match
        if self.not_match is not None:
            params[f"{field}!"] = self.not_match
        if self.include is not None:
            params[field] = ",".join(map(str, self.include))
        if self.exclude is not None:
            params[f"{field}!"] = ",".join(map(str, self.exclude))
        if self.exists is True:
            params[field] = ""
        if self.exists is False:
            params[f"!{field}"] = ""
        if self.regex is not None:
            params[field] = self.regex
        if self.gt is not None:
            params[f"{field}>"] = self.gt
        if self.gte is not None:
            params[f"{field}>="] = self.gte
        if self.lt is not None:
            params[f"{field}<"] = self.lt
        if self.lte is not None:
            params[f"{field}<="] = self.lte
        return params
