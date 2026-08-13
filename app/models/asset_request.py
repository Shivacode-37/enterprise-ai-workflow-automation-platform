from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.models.approval import Approval
from app.models.workflow_run import WorkflowRun

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.orders import Order
    from app.models.approval import Approval
    from app.models.asset_request import AssetRequest

class AssetRequest(Base):
    __tablename__ = "asset_requests"
    orders: Mapped[list["Order"]] = relationship(
    back_populates="request",
)
    approvals: Mapped[list["Approval"]] = relationship(
    back_populates="request",
)
    workflow_runs: Mapped[list["WorkflowRun"]] = relationship(
    back_populates="request",
)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    request_type: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(
        String(20),
        default="NORMAL",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING",
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship(
        back_populates="asset_requests",
    )
