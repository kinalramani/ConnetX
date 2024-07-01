from datetime import datetime,timedelta
from fastapi import HTTPException,status,Security
from dotenv import load_dotenv
import os 
from jose import JWTError,jwt



load_dotenv()
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))
def get_token(id):
    payload = {
        "user_id": id,
        "exp": datetime.utcnow() + timedelta(minutes=100),
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(type(access_token))
    return access_token



def decode_token_user_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )
    


def logging_token(u_id,u_name,e_mail):
    payload = {
        "u_id" : u_id,
        "u_name" :u_name,
        "e_mail" : e_mail,
        "exp" : datetime.utcnow() + timedelta(minutes=100)
    }
    access_token  = jwt.encode(payload,SECRET_KEY,ALGORITHM)
    print(type(access_token))
    return access_token


def decode_token_u_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("u_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )



def decode_token_user_name(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get("u_name")
        if not user_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user not exists in payload",
            )
        return user_name
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )
    


def decode_token_user_password(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_password = payload.get("password")
        if not user_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_password
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )
    




# def logging_token(id,u_name,e_mail):
#     payload = {
#         "id" : id,
#         "u_name" :u_name,
#         "e_mail" : e_mail,
#         "exp" : datetime.utcnow() + timedelta(minutes=5)
#     }
#     access_token  = jwt.encode(payload,SECRET_KEY,ALGORITHM)
#     print(type(access_token))
#     return access_token
