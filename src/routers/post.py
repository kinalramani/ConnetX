from fastapi import APIRouter,HTTPException,Header
from src.models.user import User
from src.models.post import Post
from src.schemas.post import PostCreate
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import decode_token_u_id
from logs.log_config import logger
import uuid
from src.schemas.post import Comment




userpost=APIRouter()

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


#-------------------------------------------------------create post---------------------------

    
@userpost.post("/create_post",response_model=PostCreate)
def create_post(post: PostCreate, token = Header(...)):
    user_id = decode_token_u_id(token)
    logger.info("Attempting to find user id from user table")
    db_user = db.query(User).filter(User.id == user_id,User.is_active == True,User.is_deleted == False, User.is_verified == True).first()

    if not db_user:
        logger.info("user not found")
        raise HTTPException(status_code=403, detail="User not found")
    

    active_tags = []

    find_tag_username = db.query(User).filter(User.is_active == True,User.is_deleted == False , User.is_verified == True).all()
    # breakpoint()
    found_uname_lst = []

    for each_entry in find_tag_username:
        found_uname_lst.append(each_entry.u_name)    

    
    for user_name_in_post in post.tags:
        if not user_name_in_post in found_uname_lst:
            raise HTTPException(status_code=404,detail="User name not found")


    db_post = Post(
        id=str(uuid.uuid4()),
        user_id = user_id ,
        type=post.type, 
        comment=[],
        caption = post.caption,
        music = post.music,
        title = post.title,
        tags=post.tags,
        like = []
    )
    logger.info(f"Creating post for user_id: {user_id}")
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    logger.success(f"Post created successfully with id: {db_post.id}")

    return db_post



#------------------------------------------------get post---------------------------------------


@userpost.get("/get_posts")
def get_post(post_id: str):
    logger.info(f"Fetching post with id: {post_id}")
    post = db.query(Post).filter(Post.id == post_id, Post.is_active == True, Post.is_deleted == False).first()
    if not post:
        logger.warning(f"Post with id {post_id} not found or is inactive/deleted")
        raise HTTPException(status_code=404, detail="Post not found")
    logger.success(f"Post with id {post_id} found and is active")
    return post



#-------------------------------------------Update post using put-------------------------------------

@userpost.put("/update_post_using_put")
def update_post(post_id: str, post: PostCreate, token = Header(...)):
    user_id = decode_token_u_id(token)
    logger.info(f"User {user_id} is attempting to update post {post_id}")
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if not db_post:
        logger.warning(f"Post with id {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_post.user_id != db_user.id:
        logger.warning(f"User {user_id} is not authorized to update post {post_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    db_post.type = post.type
    db_post.music = post.music
    db_post.caption = post.caption
    db_post.title =post.title
    
    
    db.commit()
    db.refresh(db_post)

    logger.success(f"Post {post_id} successfully updated by user {user_id}")
    return db_post





#-------------------------------------------Update post using patch-------------------------------------

@userpost.patch("/update_post_using_patch")
def update_post(post_id: str, post: PostCreate, token = Header(...)):
    user_id = decode_token_u_id(token)
    logger.info(f"User {user_id} is attempting to update post {post_id}")
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if not db_post:
        logger.warning(f"Post with id {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_post.user_id != db_user.id:
        logger.warning(f"User {user_id} is not authorized to update post {post_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    db_post.type = post.type
    db_post.music = post.music
    db_post.caption = post.caption
    db_post.title =post.title
    
    
    db.commit()
    db.refresh(db_post)

    logger.success(f"Post {post_id} successfully updated by user {user_id}")
    return db_post




#---------------------------------------------------delete post---------------------------------

@userpost.delete("/delete_post")
def delete_post(post_id: str, token = Header(...)):
    user_id = decode_token_u_id(token)
    logger.info(f"User {user_id} is attempting to delete post {post_id}")
    db_post = db.query(Post).filter(Post.id == post_id,Post.is_active == True,Post.is_deleted == False).first()

    if not db_post:
        logger.warning(f"Post with id {post_id} not found or is already inactive/deleted")
        raise HTTPException(status_code=404, detail="Post not found")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_post.user_id != db_user.id:
        logger.warning(f"User {user_id} is not authorized to delete post {post_id}")
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    db_post.is_active = False
    db_post.is_deleted = True
    db.commit()

    logger.success(f"Post {post_id} successfully deleted by user {user_id}")
    return {"detail": "Post deleted successfully"}




#-----------------------------------------------------like/dislike-------------------------------------------

@userpost.post("/like_dislike_post")
def like_dislike_post(post_id: str, token: str = Header(...)):
    db_user_id = decode_token_u_id(token)
    logger.info(f"User {db_user_id} is attempting to like/dislike post {post_id}")
    db_user = db.query(User).filter(User.id == db_user_id, User.is_active == True, User.is_deleted == False, User.is_verified == True).first()
    if db_user is None:

        logger.warning(f"User {db_user_id} not found or inactive/deleted")
        raise HTTPException(status_code=404, detail="User not found")
   
    db_post = db.query(Post).filter(Post.id == post_id, Post.is_active == True, Post.is_deleted == False).first()
    if db_post is None:
        logger.warning(f"Post with id {post_id} not found or inactive/deleted")
        raise HTTPException(status_code=404, detail="post not found")
   
    if db_user_id in db_post.like:
        logger.warning(f"User {db_user_id} has already liked post {post_id}")
        raise HTTPException(status_code=400, detail="You have already liked this post")
    

    likes_list=[]
    likes_list=db_post.like.copy()
    likes_list.append(db_user_id)
    db_post.like=likes_list


    db.commit()
    db.refresh(db_post) 

    logger.success(f"User {db_user_id} successfully liked post {post_id}")
    return {"detail": "Successfully liked the post"}




 #---------------------------------------------------------likes count--------------------------------------   
    
@userpost.get("/likes_count")
def following_count(post_id:str):
    logger.info(f"Fetching likes count for post {post_id}")
    db_user=db.query(Post).filter(Post.id == post_id,Post.is_active == True,Post.is_deleted == False).first()

    if db_user is None:
        logger.warning(f"Post with id {post_id} not found or inactive/deleted")
        raise HTTPException(status_code=404,detail="User not found")
    
    likes_count=len(db_user.like)

    logger.success(f"Post {post_id} has {likes_count} likes")
    return {"user_id": post_id, "likes_count": likes_count}
   




#----------------------------------------------------------Add comment------------------------------------------





@userpost.post("/add_comment")
def add_comment(comment_data: Comment,token=Header(...)):
    db_user_id = decode_token_u_id(token)
    logger.info(f"User {db_user_id} is attempting to add a comment to post {comment_data.post_id}")
    db_user = db.query(User).filter(User.id == db_user_id, User.is_active == True, User.is_deleted == False, User.is_verified == True).first()

    if not db_user:
        logger.warning(f"User {db_user_id} not found or inactive/deleted")
        raise HTTPException(status_code=404, detail="User not found")

    db_post = db.query(Post).filter(Post.id == comment_data.post_id).first()

    if not db_post:
        logger.warning(f"Post with id {comment_data.post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")

    new_list=[]


    if db_post.comment:
            list_of_comment = db_post.comment.copy()
            logger.warning(f"Post with id {comment_data.post_id} not found")
            list_of_comment.append(
                {"user_id": db_user_id,"comment": comment_data.comment}
            )
            db_post.comment = list_of_comment
            db.add(db_post)
            db.commit()

    else:
            list_of_comment = []

            logger.info(f"Creating new comment list for post {comment_data.post_id} with comment by user {db_user_id}")
            list_of_comment.append(
                {"user_id": db_user_id, "comment": comment_data.comment}
            )
            db_post.comment = list_of_comment
            db.add(db_post)
            db.commit()

            logger.success(f"Comment by user {db_user_id} successfully added to post {comment_data.post_id}")
    return {"message": "Comment added successfully"}





#----------------------------------------------------------------------Find user id of post's comments-----------

@userpost.get("/find_user_id_of_posts_comments")
def find_user_id_of_posts_comments(token = Header(...)):
    user_id=decode_token_u_id(token)
    logger.info(f"User {user_id} is attempting to find their comments on posts")
    db_user=db.query(User).filter(User.id == user_id,User.is_active == True,User.is_deleted == False,User.is_verified == True).first()

    if not db_user:
        logger.warning(f"User {user_id} not found or inactive/deleted")
        raise HTTPException(status_code=404,detail= "user not found")
    
    db_post = db.query(Post).filter(Post.is_active == True , Post.is_deleted == False).all()

    if db_post is None:
        logger.warning("No active posts found")
        raise HTTPException(status_code=404,detail="post not found")

    logger.info(f"Checking comments for user {user_id} in {len(db_post)} posts")
    empty_list=[]
    breakpoint()

    for single_post in db_post:
        for each_comment in single_post.comment:
            if user_id in each_comment['user_id']:
                logger.info(f"User {user_id} commented on post {single_post.id}")
                empty_list.append(single_post.id)
                break

    logger.success(f"User {user_id} has commented on {len(empty_list)} posts")
    return empty_list



    