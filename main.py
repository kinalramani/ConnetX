from fastapi import FastAPI
from src.routers.user import userauth
from src.routers.user import Otp_router
from src.routers.post import userpost
from src.routers.story import userstory



app=FastAPI()


app.include_router(userauth)
app.include_router(Otp_router)
app.include_router(userpost)
app.include_router(userstory)
