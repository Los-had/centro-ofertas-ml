from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True,
    )

    score: Mapped[float] = mapped_column(Float)
    discount_percent: Mapped[float] = mapped_column(Float, default=0)

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
    )

    reason: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    product = relationship("Product", back_populates="deals")
