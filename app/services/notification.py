from typing import Protocol

class EmailSender(Protocol):
    def send_email(
        self,
        *,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        ...
        
class ConsoleEmailSender:
    def send_email(
        self,
        *,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        print(f'Email to: {to_email}')
        print(f'Subject: {subject}')
        print(body)