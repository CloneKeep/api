# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from uuid import UUID
# from typing import Optional
# 
# # --- Content Schemas ---
# class ContentBase(BaseModel):
#     content: Optional[str] = None
#     status: int = 0
# 
# class ContentCreate(ContentBase):
#     created_id: str
#     updated_id: str
# 
# class ContentUpdate(BaseModel):
#     content: Optional[str] = None
#     status: Optional[int] = None
#     updated_id: str
# 
# class ContentResponse(ContentBase):
#     cid: UUID
#     created_at: datetime
#     created_id: str
#     updated_at: datetime
#     updated_id: str
# 
#     class Config:
#         from_attributes = True
# 
