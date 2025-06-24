from abc import ABC, abstractmethod

class EmailSender(ABC):
    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str) -> None:
        pass

"""
from email.sender_factory import get_email_sender
from email.template_registry import get_email_body

def send_magic_link(to_email: str, link: str):
    subject = "Your Magic Login Link"
    body = get_email_body("magic_link", link=link)
    sender = get_email_sender()
    sender.send_email(to_email, subject, body)
"""