from dataclasses import dataclass
from typing import Any

from lotr_sdk.schemas.base import (
    BaseFilters,
    BaseResource,
    FieldFilter,
    PaginatedResponse,
)


class Quote(BaseResource):
    dialog: str
    movie: str
    character: str


class QuoteList(PaginatedResponse[Quote]):
    pass


@dataclass
class QuoteFilters(BaseFilters):
    dialog: FieldFilter | None = None
    movie: FieldFilter | None = None
    character: FieldFilter | None = None

    def to_dict(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.dialog is not None:
            params.update(self.dialog.to_dict("dialog"))
        if self.movie is not None:
            params.update(self.movie.to_dict("movie"))
        if self.character is not None:
            params.update(self.character.to_dict("character"))
        return params
