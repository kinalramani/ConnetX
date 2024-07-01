from pydantic import BaseModel,EmailStr
from typing import List,Optional




class PostCreate(BaseModel):

    type : str 
    caption : str
    title : str
    music : str
    tags : list
    

class Comment(BaseModel):
    comment: str
    post_id: str



    