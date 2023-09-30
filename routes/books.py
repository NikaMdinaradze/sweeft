from fastapi import APIRouter, Depends, Query, UploadFile,File
from database import Session, get_db
from JWT import get_current_user
from typing import List
from CRUD import books
import schemas

router = APIRouter(
    tags=['books'],
    prefix='/books'
)

@router.post("/")
def create_book(title:str,
                author:str,
                genre:str,
                description:str,
                location:str,
                condition:str,
                photo: UploadFile = File(...),
                user:str = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):
    
    return books.create_book(title,author,genre,description,location,condition,photo,user,db)


@router.get('/', response_model=List[schemas.Book])
def filter_and_search(
    query: str = Query(None, description="Search query"),
    genre: str = Query(None, description="Category filter"),
    db: Session = Depends(get_db)
):
    return books.filter_and_search(query,genre,db)

@router.patch('/{id}')
def update_books(id:int,condition:str, db:Session = Depends(get_db), user:str = Depends(get_current_user)):
    return books.update_books(id,condition, db, user)

@router.delete('/{id}')
def delete_books(id, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return books.delete_books(id, user['id'], db) 
