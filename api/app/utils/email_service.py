import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException, Request
from starlette.requests import Request as StarletteRequest
from app.config import settings
import logging

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")


class Email:
    def __init__(self):
        self.username = settings.MAIL_USERNAME
        self.password = settings.MAIL_PASSWORD
        self.server = settings.MAIL_SERVER
        self.port = settings.MAIL_PORT
        self.use_ssl = settings.MAIL_SSL_TLS

    def send_email(self, to_email: str, subject: str, content: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(content, 'html'))

            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.server, self.port)
            else:
                server = smtplib.SMTP(self.server, self.port)
                server.starttls()

            server.login(self.username, self.password)
            server.sendmail(self.username, to_email, msg.as_string())
            server.quit()
            logger.info(f"Email sent to {to_email} with subject '{subject}'")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    def send_registration_email(self, request: Request, username: str, email: str, password: str):
        template = templates.TemplateResponse("registration_email.html", {
            "request": request,
            "username": username,
            "email": email,
            "password": password
        })
        content = template.body.decode('utf-8')
        self.send_email(email, "Registration Successful", content)

    def send_reset_password_email(self, request: Request, email: str, new_password: str):
        template = templates.TemplateResponse("reset_password_email.html", {
            "request": request,
            "new_password": new_password
        })
        content = template.body.decode('utf-8')
        self.send_email(email, "Password Reset Request", content)

    def send_startup_email(self):
        request = StarletteRequest(scope={"type": "http"})
        template = templates.TemplateResponse("startup_email.html", {"request": request})
        content = template.body.decode('utf-8')
        self.send_email(settings.MAIL_FROM, "Server Startup Notification", content)


email_service = Email()
