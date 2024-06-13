from typing import Tuple, List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc

from app import Product
from app.serializers import products as sp


async def get_products(async_session: AsyncSession, item: sp.GetProductRequest) -> tuple[list[dict[str, Any]], int]:
    query = select(Product)
    if item.search:
        query = query.where(Product.name.ilike(f"%{item.search}%"))
    if item.desc:
        query = query.order_by(desc(getattr(Product, item.order_by.value)))
    else:
        query = query.order_by(getattr(Product, item.order_by.value))
    check_email_history = await async_session.execute(
        query.offset(item.offset * item.limit).limit(item.limit)
    )

    email_histories = check_email_history.scalars().all()
    # Query for total record count
    total_count = await async_session.execute(query)
    total_records = len(total_count.scalars().all())
    result = []
    for email_history in email_histories:
        result.append(sp.ProductInfoSerializer.from_orm(email_history).dict())
    return result, total_records
