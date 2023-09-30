from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password):
    return pwd_cxt.hash(password)

def verify(plain_password,hashed_password):
    return pwd_cxt.verify(plain_password,hashed_password)