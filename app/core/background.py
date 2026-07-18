import logging

logger = logging.getLogger(__name__)

def log_order_status_changed(
    order_id: int,
    status: str,
) -> None:
    logger.info(
        'Order Status changed: order_id=%s status=%s',
        order_id,
        status,
    )