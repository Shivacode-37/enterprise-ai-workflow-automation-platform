from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.asset_request import AssetRequest


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    workflow_runs: Mapped[list["WorkflowRun"]] = relationship(
    back_populates="request",
)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    request_id: Mapped[int] = mapped_column(
        ForeignKey("asset_requests.id"),
        nullable=False,
        index=True,
    )

    workflow_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="RUNNING",
        index=True,
    )

    current_step: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    request: Mapped["AssetRequest"] = relationship(
        back_populates="workflow_runs",
    )
