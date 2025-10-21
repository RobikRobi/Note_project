from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class NoteCreate(BaseModel):
    title: Optional[List[str]] = None  # список тегов
    content: Optional[str] = None



class NoteUpdate(BaseModel):
    content: Optional[str] = None
    title: Optional[List[str]] = None