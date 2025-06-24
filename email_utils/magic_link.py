from email.sender_factory import get_email_sender
from email.template_registry import get_email_body

def send_magic_link_email(to_email: str, link: str):
    subject = "Your Magic Login Link"
    body = get_email_body("magic_link", link=link)
    sender = get_email_sender()
    sender.send_email(to_email, subject, body)