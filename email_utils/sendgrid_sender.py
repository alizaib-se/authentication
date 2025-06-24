import sendgrid
from sendgrid.helpers.mail import Mail
from config import Config
from .base import EmailSender

class SendGridSender(EmailSender):
    def send_email(self, to_email: str, subject: str, body: str) -> None:
        sg = sendgrid.SendGridAPIClient(api_key=Config.EMAIL_CONFIG["sendgrid"]["api_key"])
        message = Mail(
            from_email='no-reply@example.com',
            to_emails=to_email,
            subject=subject,
            html_content=body
        )
        sg.send(message)
