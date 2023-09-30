from fastapi import UploadFile, File,Depends,APIRouter,Query
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db, Session
from JWT import get_current_user
from CRUD import users
from typing import List
import schemas


router = APIRouter(
    tags=['users'],
    prefix="/users"
)

UPLOAD_FOLDER = "static\profiles"



@router.post('/')
def registration(username: str, email: str, password: str, profile: UploadFile = File(...), db: Session = Depends(get_db)):
    return users.registration(username, email,password, profile,db)

@router.post('/login')
def login(response: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return users.login(response,db)


@router.get("/", response_model= List[schemas.UserWithBooks])
def search_user(
    id: int = Query(None, description="Get User With ID"),
    query: str = Query(None, description="Search User With Username"),
    db: Session = Depends(get_db)
):
    return users.search_user(id, query,db)


@router.get('/me', response_model=schemas.User)
def me(user:str = Depends(get_current_user), db:Session = Depends(get_db)):
    return users.me(user, db)

@router.patch("/")
def update_password(new_password: str, old_password: str,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    return users.update_password(new_password,old_password,user,db)

@router.delete('/')
def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return users.delete_user(user, db)
