from typing import Annotated

from pydantic import AliasChoices, Field

MongoIdField = Annotated[
    str, Field(description="MongoDB ObjectId", validation_alias=AliasChoices("_id", "id"), serialization_alias="id")
]
