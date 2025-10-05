from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# -------------------------
# Product Model
# -------------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    movements = db.relationship('ProductMovement', backref='product', lazy=True)

# -------------------------
# Location Model
# -------------------------
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

# -------------------------
# Product Movement Model
# -------------------------
class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    from_location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    to_location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    qty = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional: backrefs for locations
    from_location_obj = db.relationship('Location', foreign_keys=[from_location], lazy=True)
    to_location_obj = db.relationship('Location', foreign_keys=[to_location], lazy=True)
