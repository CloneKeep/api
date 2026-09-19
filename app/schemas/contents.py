from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional

# --- Content Schemas ---
class ContentBase(BaseModel):
    note_id: UUID
    content: Optional[str] = None
    position: Optional[int] = 0
    is_checked: Optional[bool] = False

# class ContentCreate(ContentBase):
#     created_id: str
#     updated_id: str

class ContentUpdate(BaseModel):
    content: Optional[str] = None
    position: Optional[int] = 0
    is_checked: Optional[bool] = False

class ContentResponse(ContentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

