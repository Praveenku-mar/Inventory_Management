from app import app, db
from models import Product, Location, ProductMovement
from datetime import datetime
import random

with app.app_context():
    # ------------------
    # Clear existing data
    # ------------------
    db.drop_all()
    db.create_all()

    # ------------------
    # Add Products
    # ------------------
    products = [
        Product(id='P001', name='Product A', description='First product'),
        Product(id='P002', name='Product B', description='Second product'),
        Product(id='P003', name='Product C', description='Third product'),
        Product(id='P004', name='Product D', description='Fourth product')
    ]
    db.session.add_all(products)

    # ------------------
    # Add Locations
    # ------------------
    locations = [
        Location(id='L001', name='Warehouse X'),
        Location(id='L002', name='Warehouse Y'),
        Location(id='L003', name='Shop 1'),
        Location(id='L004', name='Shop 2')
    ]
    db.session.add_all(locations)
    db.session.commit()

    # ------------------
    # Deterministic Movements (first 15)
    # ------------------
    movements = [
        ProductMovement(product_id='P001', from_location=None, to_location='L001', qty=100),
        ProductMovement(product_id='P001', from_location='L001', to_location='L002', qty=30),
        ProductMovement(product_id='P001', from_location='L002', to_location='L003', qty=20),
        ProductMovement(product_id='P002', from_location=None, to_location='L001', qty=80),
        ProductMovement(product_id='P002', from_location='L001', to_location='L004', qty=40),
        ProductMovement(product_id='P003', from_location=None, to_location='L002', qty=60),
        ProductMovement(product_id='P003', from_location='L002', to_location='L003', qty=30),
        ProductMovement(product_id='P003', from_location='L003', to_location=None, qty=10),
        ProductMovement(product_id='P004', from_location=None, to_location='L004', qty=50),
        ProductMovement(product_id='P004', from_location='L004', to_location='L001', qty=25),
        ProductMovement(product_id='P001', from_location='L001', to_location='L004', qty=10),
        ProductMovement(product_id='P002', from_location='L004', to_location='L002', qty=15),
        ProductMovement(product_id='P003', from_location='L003', to_location='L001', qty=5),
        ProductMovement(product_id='P004', from_location='L001', to_location='L002', qty=20),
        ProductMovement(product_id='P001', from_location='L002', to_location='L003', qty=25),
    ]

    # ------------------
    # Random extra movements to reach 20
    # ------------------
    for _ in range(5):
        p = random.choice(products)
        
        # Pick from_location safely
        from_loc = random.choice(locations + [None])
        f = from_loc.id if from_loc else None

        # Pick to_location safely (ensure not same as from_location)
        possible_to = [loc for loc in locations if loc != from_loc] + [None]
        to_loc = random.choice(possible_to)
        t = to_loc.id if to_loc else None

        # Ensure at least one location is set
        if f is None and t is None:
            t = random.choice(locations).id

        qty = random.randint(5, 50)
        movements.append(ProductMovement(product_id=p.id, from_location=f, to_location=t, qty=qty))

    db.session.add_all(movements)
    db.session.commit()

    print("✅ Sample data added successfully!")
