from app import app, db
from models import Product, Location, ProductMovement, User
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

with app.app_context():
    db.drop_all()
    db.create_all()

    # Admin User
    admin = User(username="admin", email="admin@example.com", password=generate_password_hash("password"))
    db.session.add(admin)

    # Products
    products = [
        Product(name="Product A", description="Description A"),
        Product(name="Product B", description="Description B"),
        Product(name="Product C", description="Description C"),
        Product(name="Product D", description="Description D"),
    ]
    db.session.add_all(products)

    # Locations
    locations = [
        Location(name="Warehouse X"),
        Location(name="Warehouse Y"),
        Location(name="Warehouse Z"),
    ]
    db.session.add_all(locations)
    db.session.commit()

    # Movements
    movements = []
    for _ in range(20):
        product = random.choice(products)
        from_loc = random.choice(locations + [None])
        to_loc = random.choice(locations + [None])
        if from_loc == to_loc:
            to_loc = None if from_loc else random.choice(locations)
        qty = random.randint(1, 50)
        timestamp = datetime.utcnow() - timedelta(days=random.randint(0, 30))
        movement = ProductMovement(
            product_id=product.id,
            from_location=from_loc.id if from_loc else None,
            to_location=to_loc.id if to_loc else None,
            qty=qty,
            timestamp=timestamp
        )
        movements.append(movement)

    db.session.add_all(movements)
    db.session.commit()
    print("Seeding complete! Admin login: admin@example.com / password")
