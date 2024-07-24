from pydantic import BaseModel


class Comment(BaseModel):
    name: str
    email: str
    movie_id: str
    text: str
    date: str
