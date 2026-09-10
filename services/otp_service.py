import random
import smtplib

from email.mime.text import MIMEText


otp_store = {}


def generate_otp():

    return str(
        random.randint(100000, 999999)
    )


def save_otp(email, otp):

    otp_store[email] = otp


def verify_otp(email, otp):

    stored_otp = otp_store.get(email)

    if stored_otp == otp:

        del otp_store[email]

        return True

    return False


def send_otp(email, otp, smtp_host, smtp_port,
             smtp_username, smtp_password):

    message = MIMEText(
        f"""
Your Pothole Detection verification OTP is:

{otp}

This OTP is valid for your signup verification.
"""
    )

    message["Subject"] = "Pothole Detection - Email Verification"
    message["From"] = smtp_username
    message["To"] = email

    with smtplib.SMTP(
        smtp_host,
        smtp_port
    ) as server:

        server.starttls()

        server.login(
            smtp_username,
            smtp_password
        )

        server.send_message(message)    