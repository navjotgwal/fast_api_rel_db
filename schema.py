from pydantic import BaseModel


class Movie(BaseModel):
    id = int
    name = str
    desc = str
    type = str
    url = str
    rating = int

    class Config:
        orm_mode = True
