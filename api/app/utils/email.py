from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from app.config import settings
from starlette.requests import Request as StarletteRequest
import logging

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")


def send_email(to_email: str, subject: str, content: str):
    message = Mail(
        from_email=settings.MAIL_FROM,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent to {to_email} with subject '{subject}'")
        return response
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


def send_registration_email(request: Request, username: str, email: str, password: str):
    template = templates.TemplateResponse("registration_email.html", {
        "request": request,
        "username": username,
        "email": email,
        "password": password
    })
    content = template.body.decode('utf-8')
    send_email(email, "Registration Successful", content)


def send_reset_password_email(request: Request, email: str, new_password: str):
    template = templates.TemplateResponse("reset_password_email.html", {
        "request": request,
        "new_password": new_password
    })
    content = template.body.decode('utf-8')
    send_email(email, "Password Reset Request", content)


def send_startup_email():
    request = StarletteRequest(scope={"type": "http"})
    template = templates.TemplateResponse("startup_email.html", {"request": request})
    content = template.body.decode('utf-8')
    send_email(settings.MAIL_FROM, "Server Startup Notification", content)
