from fastapi import status, HTTPException
from forms import UploadPhoto
from sqlalchemy import or_
import models
import os

UPLOAD_FOLDER = "static/books"

def create_book(title,author,genre,description,location,condition,photo,user,db):
    
    url = UploadPhoto(photo, "books")
    
    new_book = models.Books(title = title,
                            author=author,
                            owner_id=user["id"],
                            genre = genre,
                            description = description,
                            location = location,
                            condition = condition,
                            photo = url)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {"detail": "Book Has Created", "status":status.HTTP_201_CREATED}

def filter_and_search(query,genre,db):
    search_conditions = (
        models.Books.title.ilike(f"%{query}%"),
        models.Books.description.ilike(f"%{query}%"),
        models.Books.author.ilike(f"%{query}%")
    )

    books = db.query(models.Books)

    if genre:
        books = books.filter(models.Books.genre == genre)
    
    if query:
        books = books.filter(or_(*search_conditions))
    
    books = books.all()
    return books

def update_books(id,condition, db, user):
    book = db.query(models.Books).get(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book Doesn't Exist")
    if not book.owner_id == user['id']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")

    book.condition = condition
    db.commit()

    return {"detail": "Book's Condition Has Updated", 'status':status.HTTP_202_ACCEPTED}

def delete_books(id, user_id, db):
    book = db.query(models.Books).get(id)

    if not book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book Doesn't Exist")

    if not book.owner_id == user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")
    
    if book.photo:
            file_path = os.path.join(UPLOAD_FOLDER, os.path.basename(book.photo))
            if os.path.exists(file_path):
                os.remove(file_path)

    book_requests = db.query(models.Requests).filter(models.Requests.book_id == id).all()

    for request in book_requests:
        db.delete(request)
        db.commit()

    db.delete(book)
    db.commit()
    return {'detail': 'Book Has Deleted', 'status': status.HTTP_204_NO_CONTENT}
