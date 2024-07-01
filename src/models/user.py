from sqlalchemy import Column,String,Boolean,DateTime,JSON
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime





class User(Base):
    __tablename__="users"
    id=Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    f_name=Column(String(100),nullable=False)
    l_name=Column(String(100),nullable=False)
    u_name=Column(String(100),nullable=False)
    e_mail=Column(String(200),nullable=False)
    password=Column(String(100),nullable=False)
    birth_date=Column(String(50),nullable=False)
    mo_number=Column(String(10),nullable=False)
    is_deleted=Column(Boolean,default=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now)
    modified_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    is_verified=Column(Boolean,default=False)
    followers = Column(JSON)
    following = Column(JSON)





   

