from sqlalchemy import Column,String,Boolean,DateTime,ForeignKey,Integer,Text,JSON
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime





class Post(Base):
    __tablename__="post"
    id=Column(String(100),primary_key=True,default=str(uuid.uuid4))
    user_id=Column(String(100),ForeignKey('users.id'),nullable=False)
    type = Column(String(50))  
    comment = Column(JSON)
    title=Column(String(100),nullable=False)
    like = Column(JSON) 
    is_deleted=Column(Boolean,default=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now)
    modified_at=Column(DateTime,default=datetime.now,onupdate=datetime.now) 
    music = Column(String(255), nullable=True) 
    caption = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True) 
    
                                                                                      