from .. import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

# flask db migrate -m "create fuel_purchases table"
# flask db upgrade 
class FuelPurchase(db.Model):
    __tablename__ = "fuel_purchases"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    liters = db.Column(
        db.Float(),
        nullable=False,
        unique=False
    )

    cost = db.Column(
        db.Float(),
        default=0.00,
        nullable=False,
        unique=False
    )

    # Foreign Key
    tower_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("towers.id", ondelete="CASCADE")
    )

    # Get an instance of an tower via tower attribute
    tower = db.relationship("Tower", back_populates="fuel_purchases")

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "liters": self.liters,
            "cost": self.cost,
            "tower_id": self.tower_id,
            "tower_name": self.tower.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }