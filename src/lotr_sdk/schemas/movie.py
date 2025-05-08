"""Movie schemas for the LOTR SDK."""

from dataclasses import dataclass
from typing import Any

from pydantic import Field

from lotr_sdk.schemas.base import BaseResource, FieldFilter, PaginatedResponse


class Movie(BaseResource):
    """A movie in the Lord of the Rings universe.

    Attributes:
        id: Unique identifier of the movie
        name: Name of the movie
        runtimeInMinutes: Runtime of the movie in minutes
        budgetInMillions: Budget of the movie in millions
        boxOfficeRevenueInMillions: Box office revenue in millions
        academyAwardNominations: Number of Academy Award nominations
        academyAwardWins: Number of Academy Award wins
        rottenTomatoesScore: Rotten Tomatoes score
    """

    name: str
    runtime_in_minutes: int = Field(..., alias="runtimeInMinutes")
    budget_in_millions: float = Field(..., alias="budgetInMillions")
    box_office_revenue_in_millions: float = Field(..., alias="boxOfficeRevenueInMillions")
    academy_award_nominations: int = Field(..., alias="academyAwardNominations")
    academy_award_wins: int = Field(..., alias="academyAwardWins")
    rotten_tomatoes_score: float = Field(..., alias="rottenTomatoesScore")


MovieList = PaginatedResponse[Movie]


@dataclass
class MovieFilters:
    """Filter options for movie queries.

    Attributes:
        name: Filter by movie name (exact match)
        runtime_in_minutes: Filter by runtime in minutes
        budget_in_millions: Filter by budget in millions
        box_office_revenue_in_millions: Filter by box office revenue in millions
        academy_award_nominations: Filter by number of Academy Award nominations
        academy_award_wins: Filter by number of Academy Award wins
        rotten_tomatoes_score: Filter by Rotten Tomatoes score
    """

    name: FieldFilter | None = None
    runtime_in_minutes: FieldFilter | None = None
    budget_in_millions: FieldFilter | None = None
    box_office_revenue_in_millions: FieldFilter | None = None
    academy_award_nominations: FieldFilter | None = None
    academy_award_wins: FieldFilter | None = None
    rotten_tomatoes_score: FieldFilter | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert filter options to dictionary of query parameters.

        Returns:
            Dictionary of filter parameters
        """
        params: dict[str, Any] = {}

        if self.name is not None:
            params.update(self.name.to_dict("name"))
        if self.runtime_in_minutes is not None:
            params.update(self.runtime_in_minutes.to_dict("runtimeInMinutes"))
        if self.budget_in_millions is not None:
            params.update(self.budget_in_millions.to_dict("budgetInMillions"))
        if self.box_office_revenue_in_millions is not None:
            params.update(self.box_office_revenue_in_millions.to_dict("boxOfficeRevenueInMillions"))
        if self.academy_award_nominations is not None:
            params.update(self.academy_award_nominations.to_dict("academyAwardNominations"))
        if self.academy_award_wins is not None:
            params.update(self.academy_award_wins.to_dict("academyAwardWins"))
        if self.rotten_tomatoes_score is not None:
            params.update(self.rotten_tomatoes_score.to_dict("rottenTomatoesScore"))

        return params
