import smtplib
from email.mime.text import MIMEText
from config import EMAIL_CONFIG
from .base import EmailSender

class SMTPSender(EmailSender):
    def send_email(self, to_email: str, subject: str, body: str) -> None:
        smtp_conf = EMAIL_CONFIG["smtp"]
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = smtp_conf["username"]
        msg["To"] = to_email

        with smtplib.SMTP(smtp_conf["server"], smtp_conf["port"]) as server:
            server.starttls()
            server.login(smtp_conf["username"], smtp_conf["password"])
            server.sendmail(smtp_conf["username"], to_email, msg.as_string())
