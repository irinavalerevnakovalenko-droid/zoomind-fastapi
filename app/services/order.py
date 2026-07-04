from decimal import Decimal

from app.core.exceptions import OrderNotFoundError, ProductNotFoundError, ProductOutOfStockError, InvalidOrderStatusTransitionError
from app.models.order import Order
from app.repositories.order import AbstractOrderRepository
from app.repositories.product import AbstractProductRepository
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.schemas.pagination import Pagination
from app.models.enums import OrderStatus

ALLOWED_STATUS_TRANSITIONS = {
    OrderStatus.pending: {OrderStatus.paid, OrderStatus.cancelled},
    OrderStatus.paid: {OrderStatus.shipped, OrderStatus.cancelled},
    OrderStatus.shipped: {OrderStatus.delivered},
    OrderStatus.delivered: set(),
    OrderStatus.cancelled: set(),
}

class OrderService:
    def __init__(
        self,
        order_repository: AbstractOrderRepository,
        product_repository: AbstractProductRepository,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        
    async def create_order(self, user_id: int, order_data: OrderCreate) -> Order:
        items_data = []
        total_price = Decimal('0')
        for item in order_data.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if product is None:
                raise ProductNotFoundError()
            if product.stock < item.quantity:
                raise ProductOutOfStockError()
            product.stock -= item.quantity
            total_price += product.price * item.quantity
            
            items_data.append(
                {
                    'product_id': product.id,
                    'quantity': item.quantity,
                    'unit_price': product.price,
                }
            )
            
        return await self.order_repository.create(
            user_id=user_id,
            items_data=items_data,
            total_price=total_price,
        )
        
    async def get_order(
        self,
        order_id: int,
        user_id: int,
    ) -> Order:
        order = await self.order_repository.get_by_id(
            order_id=order_id,
            user_id=user_id,
        )

        if order is None:
            raise OrderNotFoundError()

        return order
    
    async def list_orders(
        self,
        user_id: int,
        pagination: Pagination,
    ) -> list[Order]:
        return await self.order_repository.list_for_user(
            user_id=user_id,
            pagination=pagination,
        )
        
    async def update_order_status(
        self,
        order_id: int,
        user_id: int,
        status_data: OrderStatusUpdate,
    ) -> Order:
        order = await self.get_order(
            order_id=order_id,
            user_id=user_id,
        )
        allowed_statuses = ALLOWED_STATUS_TRANSITIONS[order.status]

        if status_data.status not in allowed_statuses:
            raise InvalidOrderStatusTransitionError()
        
        return await self.order_repository.update_status(
            order=order,
            status=status_data.status,
        )
        
    