from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    profile_picture = Column(String)


    books = relationship("Books", back_populates="owner")

    requests = relationship("Requests", back_populates="owner")

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    description = Column(String)
    photo = Column(String)
    location = Column(String)
    condition = Column(String)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="books")

    requests = relationship("Requests", back_populates="book")

class Requests(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    apply_time = Column(DateTime, default=func.now())
    approved = Column(Boolean)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="requests")

    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship("Books", back_populates="requests")
    
