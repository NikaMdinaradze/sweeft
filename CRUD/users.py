from forms import UploadPhoto, IsValidEmail,IsValidPassword
from JWT import create_access_token, get_current_user
from fastapi import Depends,HTTPException,status
from database import get_db, Session
from hashing import hash, verify
from . import books
import models
import os


UPLOAD_FOLDER = "static\profiles"


def registration(username, email, password, profile, db):

    if not IsValidEmail(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is Not Valid")
    
    if not IsValidPassword(password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is Not Valid")

    check = db.query(models.Users).filter(models.Users.username == username).first()
    if check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The Username Already Exists")
    
    url = UploadPhoto(profile, "profiles")
    
    user = models.Users(username=username,
                 password=hash(password),
                 email=email,
                 profile_picture=url)
    db.add(user)
    db.commit()
    
    return {"detail": "User Has Created","status":status.HTTP_201_CREATED}

def login(response, db):

    user = db.query(models.Users).filter(models.Users.username == response.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Doesn't Exist")

    if verify(response.password, user.password):
        access_token = create_access_token(data={"id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

def search_user(id,query,db):
    users_query = db.query(models.Users)

    if id is not None:
        users_query = users_query.filter(models.Users.id == id)

    if query:
        users_query = users_query.filter(models.Users.username.ilike(f"%{query}%"))

    users = users_query.all()

    return users

def me(user:str = Depends(get_current_user), db:Session = Depends(get_db)):
    self = db.query(models.Users).get(user['id'])
    return self

def update_password(new_password, old_password,user,db):
    db_user = db.query(models.Users).get(user['id'])

    if not verify(old_password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Old password is incorrect",
        )
    if not IsValidPassword(new_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is Not Valid")
    
    if old_password == new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This is Old Password")
    
    new_password_hashed = hash(new_password)
    db_user.password = new_password_hashed

    db.commit()

    return {"detail": "Password has been updated", "status_code": status.HTTP_202_ACCEPTED}

def delete_user(user, db):
    db_user = db.query(models.Users).get(user['id'])

    if db_user:
        profile_picture_url = db_user.profile_picture

        if profile_picture_url:
            file_path = os.path.join(UPLOAD_FOLDER, os.path.basename(profile_picture_url))
            if os.path.exists(file_path):
                os.remove(file_path)
                
        users_books = db.query(models.Books).filter(models.Books.owner_id == user['id']).all()

        for book in users_books:
            books.delete_books(book.id, db)  # Pass the database session to the delete_books function

        db.delete(db_user)
        db.commit()

        return {"detail": "User Has Deleted", "status": status.HTTP_204_NO_CONTENT}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


