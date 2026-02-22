# models.py

from sqlalchemy import Column, Integer, String, Text
from database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)   # user or ai
    content = Column(Text)