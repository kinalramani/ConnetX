from sqlalchemy import Column,String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime




class Follower_Following(Base):
    __tablename__ = "followerfollowing"
    id=Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    user_id=Column(String(100),ForeignKey('users.id'),nullable=False)
    follower_id = Column(String(100), ForeignKey('users.id'), nullable=False)
    following_id = Column(String(100), ForeignKey('users.id'), nullable=False)
    
    follower = relationship("User", foreign_keys=[follower_id])
    following = relationship("User", foreign_keys=[following_id])
    is_deleted=Column(Boolean,default=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now)
    modified_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)