from typing import Protocol

from app.repositories.product import AbstractProductRepository
from app.repositories.user import AbstractUserRepository

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
        
class NotificationService:
    def __init__(
        self,
        user_repository: AbstractUserRepository,
        product_repository: AbstractProductRepository,
        email_sender: EmailSender,
    ):
        self.user_repository = user_repository
        self.product_repository = product_repository
        self.email_sender = email_sender
        
    async def send_repurchase_reminder(
        self,
        user_id: int,
        product_id: int,
    ) -> bool:
        user = await self.user_repository.get_by_id(user_id)
        product = await self.product_repository.get_by_id(product_id)
        
        if (
            user is None
            or product is None
            or not user.is_newsletter_enabled
        ):
            return False
        
        self.email_sender.send_email(
            to_email=user.email,
            subject='Пора пополнить запасы для питомца',
            body=(
                f'Здравствуйте, {user.username}! '
                f'Возможно, пора повторить покупку товара '
                f'"{product.name}".'
            ),
        )

        return True