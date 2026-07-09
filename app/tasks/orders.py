import asyncio

from app.core.celery_app import celery_app
from app.core.database import async_session_maker, engine
from app.repositories.order import SQLAlchemyOrderRepository
from app.repositories.product import SQLAlchemyProductRepository
from app.services.order import OrderService


async def _send_repeat_purchase_reminders() -> int:
    try:
        async with async_session_maker() as session:
            order_repository = SQLAlchemyOrderRepository(session)
            product_repository = SQLAlchemyProductRepository(session)

            service = OrderService(
                order_repository=order_repository,
                product_repository=product_repository,
            )

            return await service.send_repeat_purchase_reminders()
    finally:
        await engine.dispose()


@celery_app.task(name='orders.send_repeat_purchase_reminders')
def send_repeat_purchase_reminders() -> int:
    return asyncio.run(_send_repeat_purchase_reminders())