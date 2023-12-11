from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import settings

'''
#models.Base.metadata.create_all(bind=engine)

- This command generates all the tables in models.py when started.
- But it will just checks for the table name. If it already exists, it will do nothing and skip.
- In order to update any database changes without doing it manually, we used Alembic (data migration tool).
'''

app = FastAPI()

# CORS
origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

#root
@app.get("/")
def root():
    return {"message": "Hello World"}