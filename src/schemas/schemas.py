from pydantic import BaseModel, HttpUrl


class Urls(BaseModel):
    links: list[HttpUrl]
