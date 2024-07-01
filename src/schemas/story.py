from pydantic import BaseModel,EmailStr
from typing import List,Optional




class StoryCreate(BaseModel):

    type : str 
    music : str
    