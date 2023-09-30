from fastapi import status, HTTPException
import models

def create_requests(book_id, user, db):
    owner_id = user['id']
    request = models.Requests(owner_id = owner_id,
                              book_id = book_id,
                              approved = False)
    db.add(request)
    db.commit()
    return {"detail":"Request Has Created", "status":status.HTTP_201_CREATED}


def read_requests(book_id, db):
    requests = db.query(models.Requests).filter(models.Requests.book_id == book_id).all()
    return requests

def update_status(id, approve_status,user, db):
    request = db.query(models.Requests).get(id)

    if not request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Request Doesn't Exist")

    book = db.query(models.Books).get(request.book_id)

    if not book.owner_id == user['id']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized User")
    
    request.approved = approve_status

    return {"details":"Request Has Updated", "status":status.HTTP_202_ACCEPTED}


def delete_request(id, user,db):
    request = db.query(models.Requests).get(id)

    if not request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Request Doesn't Exist")
    
    if not request.owner_id == user['id']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")
    
    db.delete(request)
    db.commit()
    return {"detail":"Request Has Deleted", "status":status.HTTP_204_NO_CONTENT}