from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.controllers import products as pc
from app.models.base_class import get_session
from app.serializers.products import GetProductRequest
from app.utils.responses import response_paginate

router = APIRouter(prefix='', tags=["products"])


@router.get("")
async def get_products_views(
        item: GetProductRequest = Depends(),
        async_session: AsyncSession = Depends(get_session),
):
    result, totals = await pc.get_products(async_session, item)
    return response_paginate(result, item.offset, item.limit, totals)
