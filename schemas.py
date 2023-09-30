from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    username: str
    email: str
    profile_picture: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    description: str
    photo: str
    location: str
    condition:str

class Book(BookBase):
    id: int
    owner: User

    class Config:
        from_attributes = True

class RequestBase(BaseModel):
    apply_time: datetime
    approved : bool


class Request(RequestBase):
    id: int
    owner: User
    book: Book

    class Config:
        from_attributes = True

class UserWithBooks(User):
    books: List[Book] = []

class UserWithRequests(User):
    requests: List[Request] = []

class BookWithOwner(Book):
    owner: UserWithBooks

class RequestWithOwnerAndBook(Request):
    owner: UserWithRequests
    book: BookWithOwner






    