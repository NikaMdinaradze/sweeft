import uuid, re,os
from fastapi import HTTPException, status

IMAGE_EXTENSIONS = [
    "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp", "ico",
    "svg", "raw", "heif", "heic", "psd", "eps", "pcx", "tga", "hdr"
]


def FileNameGenerator(filename):
    extension = filename.split(".")[-1]
    
    if not extension in IMAGE_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is not an image")
    
    id = uuid.uuid4()
    return f"{id}.{extension}"


def UploadPhoto(photo, location):

    unique_filename = FileNameGenerator(photo.filename)
    file_path = os.path.join("static", location, unique_filename)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    url = f'/static/{location}/{unique_filename}'  
  
    return url

def IsValidPassword(password):
    condition1 = len(password)  >= 8
    condition2 = any(char.isupper() for char in password)
    condition3 = any(char.isdigit() for char in password)

    if condition1 and condition2 and condition3:
        return True
    
    return False

def IsValidEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None