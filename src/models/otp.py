from sqlalchemy import Column,String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime





class Otp(Base):
    __tablename__ = "otps"
    id=Column(String(100),primary_key=True,index=True,default=str(uuid.uuid4()))
    e_mail = Column(String(40),nullable=False)
    u_otp = Column(String(6), index=True, nullable=False)
    expires_at = Column(DateTime)
    created_at=Column(DateTime,default=datetime.now)