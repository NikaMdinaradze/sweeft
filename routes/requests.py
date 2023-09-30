from fastapi import APIRouter, Depends
from JWT import get_current_user
from database import Session
from database import get_db
from CRUD import requests


router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)

@router.post('/')
def create_requests(book_id:int, user:str = Depends(get_current_user), db:Session = Depends(get_db)):
    return requests.create_requests(book_id, user, db)

@router.get('/')
def read_requests(book_id:int, db:Session = Depends(get_db)):
    return requests.read_requests(book_id, db)

@router.patch('/{id}')
def update_status(id:int, approve_status:bool,user:str=Depends(get_current_user), db:Session = Depends(get_db)):
    return requests.update_status(id, approve_status,user, db)



@router.delete('/{id}')
def delete_request(id, user:str = Depends(get_current_user),db:Session = Depends(get_db)):
    return requests.delete_request(id,user,db)