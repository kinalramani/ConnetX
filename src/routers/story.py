from fastapi import APIRouter,HTTPException,Header
from src.models.user import User
from src.models.stories import Story
from src.schemas.story import StoryCreate
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import decode_token_u_id
from logs.log_config import logger
import uuid
from datetime import datetime,timedelta





userstory=APIRouter()

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



#-------------------------------------------------------create story---------------------------

    
@userstory.post("/create_story/",response_model=StoryCreate)
def create_post(story: StoryCreate, token = Header(...)):
    user_id = decode_token_u_id(token)
    logger.info(f"User {user_id} is attempting to create a story")
    db_user = db.query(User).filter(User.id == user_id,User.is_active == True,User.is_deleted == False, User.is_verified == True).first()

    if not db_user:
        logger.warning(f"User {user_id} not found or inactive/deleted")
        raise HTTPException(status_code=403, detail="User not found")

    expires_at = datetime.now() + timedelta(hours=24)

    db_story = Story(
        id=str(uuid.uuid4()),
        user_id = user_id,
        type=story.type, 
        music = story.music,
        expires_at=expires_at
    ) 
    

    db.add(db_story)
    db.commit()
    db.refresh(db_story)

    

    logger.success(f"Story {db_story.id} created successfully by user {user_id}")
    return db_story





#------------------------------------------------get user's story---------------------------------------


@userstory.get("/get_story")
def get_post(story_id: str):
    logger.info(f"Fetching story with ID {story_id}")
    db_story = db.query(Story).filter(Story.id == story_id, Story.is_active == True, Story.is_deleted == False).first()

    if not db_story:
        logger.warning(f"Story with ID {story_id} not found or inactive/deleted")
        raise HTTPException(status_code=404, detail="user's story not found")
    
    current_time = datetime.now()
    if current_time > db_story.expires_at:
        db_story.is_deleted = True
        db_story.is_active = False
        db_story.is_archived = True
        db.add(db_story)
        db.commit()
        logger.warning(f"Story with ID {story_id} has expired and is now marked as deleted")
        raise HTTPException(status_code=404, detail="User's story has expired and is deleted")
    
    logger.success(f"Story with ID {story_id} fetched successfully")
    return db_story



#-------------------------------------------Update story using put-------------------------------------

@userstory.put("/update_story_using_put")
def update_post(story_id: str, story: StoryCreate, token = Header(...)):
    user_id = decode_token_u_id(token)
    logger.info(f"User {user_id} is attempting to update story {story_id}")
    db_story = db.query(Story).filter(Story.id == story_id).first()

    if not db_story:
        logger.warning(f"Story with ID {story_id} not found")
        raise HTTPException(status_code=404, detail="story not found")

    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_story.user_id != db_user.id:
        logger.warning(f"User {user_id} is not authorized to update story {story_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this story")

    db_story.type = story.type
    db_story.music = story.music
    
    
    db.commit()
    db.refresh(db_story)

    logger.success(f"Story {story_id} updated successfully by user {user_id}")
    return db_story




#-------------------------------------------Update story using patch-------------------------------------

@userstory.patch("/update_story_using_patch")
def update_post(story_id: str, story: StoryCreate, token = Header(...)):
    user_id = decode_token_u_id(token)
    logger.info(f"User {user_id} is attempting to update story {story_id}")
    db_story = db.query(Story).filter(Story.id == story_id).first()

    if not db_story:
        logger.warning(f"Story with ID {story_id} not found")
        raise HTTPException(status_code=404, detail="story not found")

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_story.user_id != db_user.id:
        logger.warning(f"User {user_id} is not authorized to update story {story_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this story")

    db_story.type = story.type
    db_story.music = story.music
    
    
    db.commit()
    db.refresh(db_story)

    logger.success(f"Story {story_id} updated successfully by user {user_id}")
    return db_story



#---------------------------------------------------delete story---------------------------------

@userstory.delete("/delete_story")
def delete_story(story_id: str, token = Header(...)):
    user_id = decode_token_u_id(token)
    logger.info(f"User {user_id} is attempting to delete story {story_id}")
    db_story = db.query(Story).filter(Story.id == story_id,Story.is_active == True,Story.is_deleted == False).first()

    if not db_story:
        logger.warning(f"Story with ID {story_id} not found or already deleted")
        raise HTTPException(status_code=404, detail="story not found")

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_story.user_id != db_user.id:
        logger.warning(f"User {user_id} is not authorized to delete story {story_id}")
        raise HTTPException(status_code=403, detail="Not authorized to delete this story")

    db_story.is_active = False
    db_story.is_deleted = True
    db.commit()

    logger.success(f"Story {story_id} deleted successfully by user {user_id}")
    return {"detail": "story deleted successfully"}

