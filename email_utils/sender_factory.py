from config import Config
from email_utils.smtp_sender import SMTPSender
from email_utils.sendgrid_sender import SendGridSender

EMAIL_SENDERS = {
    "smtp": SMTPSender,
    "sendgrid": SendGridSender
}

def get_email_sender():
    provider = Config.EMAIL_CONFIG["provider"]
    sender_class = EMAIL_SENDERS.get(provider)
    if not sender_class:
        raise ValueError(f"Unsupported email provider: {provider}")
    return sender_class()
