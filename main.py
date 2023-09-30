from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from routes import users, books,requests
import models
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(users.router)
app.include_router(books.router)
app.include_router(requests.router)

app.mount('/static/profiles',StaticFiles(directory='static/profiles'), name='users')
app.mount('/static/books',StaticFiles(directory='static/books'), name='books')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)