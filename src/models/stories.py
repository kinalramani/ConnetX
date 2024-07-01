from sqlalchemy import Column,String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime,timedelta




class Story(Base):
    __tablename__ = "story"
    id=Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    user_id=Column(String(100),ForeignKey('users.id'),nullable=False)
    type = Column(String(50)) 
    is_deleted=Column(Boolean,default=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now)
    modified_at=Column(DateTime,default=datetime.now,onupdate=datetime.now) 
    music = Column(String(255), nullable=True)
    expires_at = Column(DateTime)
    is_archived = Column(Boolean,default=False,nullable=False)



   




