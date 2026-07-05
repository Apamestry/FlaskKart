from datetime import datetime

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    payment_status = db.Column(db.String(20), nullable=False, default="Completed")
    order_status = db.Column(db.String(20), nullable=False, default="Placed")

    shipping_full_name = db.Column(db.String(120), nullable=False)
    shipping_address_line1 = db.Column(db.String(200), nullable=False)
    shipping_address_line2 = db.Column(db.String(200), nullable=True)
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_state = db.Column(db.String(100), nullable=False)
    shipping_zip_code = db.Column(db.String(20), nullable=False)
    shipping_phone = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref="orders")
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order #{self.id} user={self.user_id} total={self.total_amount}>"