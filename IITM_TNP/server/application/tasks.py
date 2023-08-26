# Import necessary modules and libraries
from celery import Celery
from application.models import User
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

# Create a Celery instance
cel_app = Celery("main")

# SMTP Configuration for Mailhog
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "donot_reply@mail.com"
SENDER_PASSWORD = ""

# Define a Celery task for sending emails
@cel_app.task()
def send_mail(to_address, subject, message, attachment_file=None):
    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))  # Attach HTML message content
    
    # If an attachment file is provided, add it to the email
    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename="monthly_report.pdf")
        msg.attach(part)
    
    # Connect to the SMTP server, login, and send the email
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    
    # Return True to indicate successful email sending
    return True
