from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from src.db import get_session
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.models.NoteModel import Note, Tags, NoteTags
from src.models.UserModel import User
from src.auth.auth_utilits import authChecker
from src.notes.notes_shema import NoteCreate, NoteUpdate



app = APIRouter(prefix="/notes", tags=["Notes"])

# Создание заметки
@app.post("/note", status_code=status.HTTP_201_CREATED)
async def create_note(
    data: NoteCreate,
    current_user: User = Depends(authChecker),
    session: AsyncSession = Depends(get_session)
):
    # Создание заметки с заголовком
    new_note = Note(
        user_id=current_user.id,
        title=data.note_title,
        content=data.content
    )

    session.add(new_note)
    await session.flush()  # получаем ID до коммита

    # Обработка тегов
    for tag_name in data.tags:
        stmt = select(Tags).where(Tags.name == tag_name)
        tag = await session.scalar(stmt)

        if not tag:
            tag = Tags(name=tag_name)
            session.add(tag)
            await session.flush()

        # Связь заметки и тега
        note_tag = NoteTags(note_id=new_note.id, tagse_id=tag.id)
        session.add(note_tag)

    await session.commit()
    await session.refresh(new_note)

    return {
        "message": "Note created successfully",
        "note_id": new_note.id,
        "user_id": current_user.id,
        "title": new_note.title,
        "content": new_note.content,
        "tags": data.tags
    }

# Обновление заметки
@app.put("/note/{note_id}")
async def update_note(
    note_id: int = Path(..., gt=0),
    data: NoteUpdate = None,
    current_user: User = Depends(authChecker),
    session: AsyncSession = Depends(get_session)
):
    # Проверяем, существует ли заметка
    stmt = select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    note = await session.scalar(stmt)

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )

    # Обновляем содержимое заметки
    if data.content is not None:
        note.content = data.content

    # Если переданы теги — обновляем их
    if data.title is not None:
        # Удаляем старые связи
        await session.execute(delete(NoteTags).where(NoteTags.note_id == note.id))

        # Создаём/находим теги и связываем с заметкой заново
        for tag_name in data.title:
            # Проверяем, есть ли тег с таким именем
            stmt = select(Tags).where(Tags.name == tag_name)
            tag = await session.scalar(stmt)

            # Если нет — создаём новый тег
            if not tag:
                tag = Tags(name=tag_name)
                session.add(tag)
                await session.flush()

            # Создаём новую связь
            link = NoteTags(note_id=note.id, tagse_id=tag.id)
            session.add(link)

    await session.commit()
    await session.refresh(note)

    return {
        "message": "Note updated successfully",
        "note_id": note.id,
        "content": note.content,
        "tags": data.title
    }


# Удаление заметки по id
@app.delete("/note/{note_id}", status_code=status.HTTP_200_OK)
async def delete_note(
    note_id: int = Path(..., gt=0),
    current_user: User = Depends(authChecker),
    session: AsyncSession = Depends(get_session)
):
    # Проверяем, что заметка существует и принадлежит текущему пользователю
    stmt = select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    note = await session.scalar(stmt)

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )

    # Удаляем все связи с тегами
    await session.execute(delete(NoteTags).where(NoteTags.note_id == note.id))

    # Удаляем саму заметку
    await session.delete(note)
    await session.commit()

    return {"message": f"Note with ID {note_id} has been deleted successfully."}

# Просмотр заметки по id
@app.get("/note/{note_id}", status_code=status.HTTP_200_OK)
async def get_note_by_id(
    note_id: int = Path(..., gt=0),
    current_user: User = Depends(authChecker),
    session: AsyncSession = Depends(get_session)
):
    # Получаем заметку вместе с тегами
    stmt = (
        select(Note)
        .options(selectinload(Note.tags))
        .where(Note.id == note_id, Note.user_id == current_user.id)
    )
    note = await session.scalar(stmt)

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )

    # Возвращаем заметку и её теги
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at,
        "updated_at": note.updated_at,
        "tags": [tag.name for tag in note.tags]
    }


# Получение всех заметок пользователя
@app.get("/notes")
async def get_user_notes(
    current_user: User = Depends(authChecker),
    session: AsyncSession = Depends(get_session)
):
    # Выбираем все заметки пользователя и сразу подгружаем теги
    stmt = select(Note).where(Note.user_id == current_user.id).options(selectinload(Note.tags))
    result = await session.scalars(stmt)
    notes = result.all()

    # Формируем вывод
    notes_list = []
    for note in notes:
        notes_list.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": [tag.name for tag in note.tags],
            "created_at": note.created_at,
            "updated_at": note.updated_at
        })

    return {"notes": notes_list}