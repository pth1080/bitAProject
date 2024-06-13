import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, func, Boolean, Float
from sqlmodel import Field, Relationship, SQLModel


# async with AsyncSession(engine) as async_session:
#     product = Product(
#         name=product_name,
#         location=location,
#         sold=sold,
#         rate=rate,
#         rate_counts=rate_counts,
#         current_price=current_price,
#         original_price=original_price,
#         discount_percent=discount_percent,
#     )
#     async_session.add(product)
#     await async_session.commit()
#
# # Print the extracted information
# print(data)
class Product(SQLModel, table=True):
    __tablename__ = "product"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=False)
    current_price: int = Field(default=None, nullable=False)
    original_price: int = Field(default=None, nullable=False)
    # optional fields
    discount_percent: int = Field(default=None, nullable=True)
    rate: int = Field(default=None, nullable=True)
    rate_counts: int = Field(default=None, nullable=True)
    sold: int = Field(default=None, nullable=True)
    location: Optional[str] = Field(default=None, nullable=True)

    product_images: List["ProductImage"] = Relationship(
        back_populates='product',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan', 'uselist': True, 'lazy': 'selectin'},
    )

    created_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=datetime.datetime.now
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=datetime.datetime.now,
            onupdate=func.now()
        )
    )


class ProductImage(SQLModel, table=True):
    __tablename__ = "product_image"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(default=None, nullable=False)
    is_main: bool = Field(nullable=False, default=False)

    product_id: int = Field(foreign_key='product.id', nullable=False)
    product: Product = Relationship(
        sa_relationship_kwargs={'uselist': False, 'lazy': 'selectin'},
        back_populates="product_images",
    )

    created_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=datetime.datetime.now
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=datetime.datetime.now,
            onupdate=func.now()
        )
    )
