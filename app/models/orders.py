from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.asset_request import AssetRequest
    from app.models.shipment import Shipment


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    request_id: Mapped[int] = mapped_column(
        ForeignKey("asset_requests.id"),
        nullable=False,
        index=True,
    )

    vendor: Mapped[str] = mapped_column(String(100))

    order_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    invoice_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    order_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="CREATED",
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    request: Mapped["AssetRequest"] = relationship(
        back_populates="orders",
    )

    shipments: Mapped[list["Shipment"]] = relationship(
        back_populates="order",
    )
