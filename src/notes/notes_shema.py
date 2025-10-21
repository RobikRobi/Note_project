from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class NoteCreate(BaseModel):
    note_title: str    
    content: Optional[str] = None
    tags: Optional[List[str]] = None  # список тегов



class NoteUpdate(BaseModel):
    content: Optional[str] = None
    title: Optional[List[str]] = None