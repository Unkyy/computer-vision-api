from pydantic import BaseModel, Field


class Url(BaseModel):
    url: str = Field(example="website.com")
