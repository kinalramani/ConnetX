from fastapi import APIRouter
from src.models.otp import Otp
from database.database import sessionLocal
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime,timedelta
from config import sender_email,password



import uuid
Otp_router=APIRouter()
db= sessionLocal()


def generate_otp(email: str):
    otp_code = str(random.randint(100000, 999999))
    expiration_time = datetime.now() + timedelta(minutes=5)
    
    otp_entry = Otp(
        id = str(uuid.uuid4()),
        e_mail=email,
        u_otp=otp_code,
        expires_at=expiration_time,
    )
    db.add(otp_entry)
    db.commit()
    return otp_code

def send_otp_email(email: str, otp_code: str):
   
    subject = "Your OTP Code"
    message_text = f"Your OTP is {otp_code} which is valid for 5 minutes"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(message_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        print("Mail sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
