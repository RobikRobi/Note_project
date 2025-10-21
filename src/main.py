from fastapi import FastAPI
from src.db import engine,Base

from src.models.UserModel import User
from src.models.NoteModel import Note, NoteTags, Tags
from src.models.SessionModel import SessionUser

from src.auth.auth_router import app as auth_router
from src.notes.notes_router import app as notes_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(notes_router)
