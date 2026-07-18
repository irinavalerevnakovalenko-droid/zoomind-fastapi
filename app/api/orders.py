from fastapi import APIRouter, Depends, status, BackgroundTasks

from app.schemas.pagination import Pagination
from app.core.dependencies import get_current_active_user, get_order_service, throttle_user
from app.core.background import log_order_status_changed
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from app.services.order import OrderService

router = APIRouter(
    prefix='/orders',
    tags=['orders'],
    dependencies=[Depends(throttle_user)],
)

@router.post(
    '/',
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.create_order(
        user_id=current_user.id,
        order_data=order_data,
    )
    
@router.get(
    '/',
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
)
async def list_orders(
    pagination: Pagination = Depends(),
    current_user: User = Depends(get_current_active_user),
    service: OrderService = Depends(get_order_service),
    ):

    return await service.list_orders(
        user_id=current_user.id,
        pagination=pagination,
    )

@router.get(
    '/{order_id}',
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    service: OrderService = Depends(get_order_service),
    ):
    
    return await service.get_order(
        order_id=order_id,
        user_id=current_user.id,
    )
    
@router.patch(
    '/{order_id}/status',
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    service: OrderService = Depends(get_order_service),
):
    updated_order = await service.update_order_status(
        order_id=order_id,
        user_id=current_user.id,
        status_data=status_data,   
    )
    
    background_tasks.add_task(
        log_order_status_changed,
        order_id=updated_order.id,
        status=updated_order.status.value,
    )
    
    return updated_order