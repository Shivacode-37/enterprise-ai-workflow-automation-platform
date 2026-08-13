from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.asset_request import AssetRequest
    from app.models.approval import Approval
class User(Base):
    __tablename__ = "users"
    asset_requests: Mapped[list["AssetRequest"]] = relationship(
    back_populates="user",
)
    approvals_given: Mapped[list["Approval"]] = relationship(
    back_populates="approver",
)
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role : Mapped[str] = mapped_column(String(50))
    department : Mapped[str | None] = mapped_column(String(50), nullable = True)
    manager_id : Mapped[str | None] = mapped_column(String(50), nullable= True)
    is_active : Mapped[bool] = mapped_column(Boolean, default= True)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
)

