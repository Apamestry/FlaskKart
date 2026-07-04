"""
Temporary helper to seed sample products for local testing.
This is NOT part of the app itself — run it manually once, standalone.
Once the Admin dashboard (Sprint 9) exists, product creation happens through
the UI instead and this script can be deleted.

Usage:
    python seed_products.py
"""

from app import create_app
from app.extensions import db
from app.models.product import Product

app = create_app()

SAMPLE_PRODUCTS = [
    {"name": "Wireless Mouse", "description": "Ergonomic wireless mouse with USB receiver.", "price": 19.99, "stock": 50},
    {"name": "Mechanical Keyboard", "description": "RGB backlit mechanical keyboard, blue switches.", "price": 59.99, "stock": 30},
    {"name": "USB-C Hub", "description": "7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader.", "price": 34.99, "stock": 0},
    {"name": "Laptop Stand", "description": "Adjustable aluminum laptop stand, foldable.", "price": 24.99, "stock": 75},
]

with app.app_context():
    for data in SAMPLE_PRODUCTS:
        exists = Product.query.filter_by(name=data["name"]).first()
        if not exists:
            db.session.add(Product(**data))
    db.session.commit()
    print(f"Seeded {len(SAMPLE_PRODUCTS)} products (skipped any that already existed).")