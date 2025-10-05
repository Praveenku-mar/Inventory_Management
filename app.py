from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Product, Location, ProductMovement
from forms import ProductForm, LocationForm, MovementForm
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -------------------------
# Home / Dashboard
# -------------------------
@app.route('/')
def index():
    products = Product.query.all()
    locations = Location.query.all()
    movements = ProductMovement.query.all()
    total_stock = sum([
        sum([m.qty if m.to_location else -m.qty for m in p.movements])
        for p in products
    ])
    return render_template('index.html', products=products, locations=locations, movements=movements, total_stock=total_stock)

# -------------------------
# Products
# -------------------------
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(id=form.id.data, name=form.name.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added!', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', form=form, product=None)

@app.route('/product/edit/<string:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', form=form, product=product)

@app.route('/product/delete/<string:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash(f'Product "{product.name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'danger')
    return redirect(url_for('products'))

# -------------------------
# Locations
# -------------------------
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/location/add', methods=['GET', 'POST'])
def add_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(id=form.id.data, name=form.name.data)
        db.session.add(location)
        db.session.commit()
        flash('Location added!', 'success')
        return redirect(url_for('locations'))
    return render_template('location_form.html', form=form, location=None)

@app.route('/location/edit/<string:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        location.name = form.name.data
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    return render_template('location_form.html', form=form, location=location)

@app.route('/location/delete/<string:location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    try:
        db.session.delete(location)
        db.session.commit()
        flash(f'Location "{location.name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting location: {str(e)}', 'danger')
    return redirect(url_for('locations'))

# -------------------------
# Product Movements
# -------------------------
@app.route('/movements')
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

@app.route('/movement/add', methods=['GET', 'POST'])
def add_movement():
    form = MovementForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]
    locs = [(l.id, l.name) for l in Location.query.all()]
    form.from_location.choices = [('', '---')] + locs
    form.to_location.choices = [('', '---')] + locs

    if form.validate_on_submit():
        from_loc = int(form.from_location.data) if form.from_location.data else None
        to_loc = int(form.to_location.data) if form.to_location.data else None

        movement = ProductMovement(
            product_id=form.product_id.data,
            from_location=from_loc,
            to_location=to_loc,
            qty=form.qty.data
        )
        db.session.add(movement)
        db.session.commit()
        flash('Movement added!', 'success')
        return redirect(url_for('movements'))
    return render_template('movement_form.html', form=form, movement=None)

@app.route('/movement/edit/<int:movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    form = MovementForm(obj=movement)
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]
    locs = [(l.id, l.name) for l in Location.query.all()]
    form.from_location.choices = [('', '---')] + locs
    form.to_location.choices = [('', '---')] + locs

    if form.validate_on_submit():
        from_loc = int(form.from_location.data) if form.from_location.data else None
        to_loc = int(form.to_location.data) if form.to_location.data else None

        movement.product_id = form.product_id.data
        movement.from_location = from_loc
        movement.to_location = to_loc
        movement.qty = form.qty.data
        db.session.commit()
        flash('Movement updated successfully!', 'success')
        return redirect(url_for('movements'))
    return render_template('movement_form.html', form=form, movement=movement)

@app.route('/movement/delete/<int:movement_id>', methods=['POST'])
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    try:
        db.session.delete(movement)
        db.session.commit()
        flash('Movement deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting movement: {str(e)}', 'danger')
    return redirect(url_for('movements'))

# -------------------------
# Report
# -------------------------
@app.route('/report')
def report():
    report_data = []
    for product in Product.query.all():
        for location in Location.query.all():
            incoming = sum([m.qty for m in product.movements if m.to_location == location.id])
            outgoing = sum([m.qty for m in product.movements if m.from_location == location.id])
            qty = incoming - outgoing
            if qty != 0:
                report_data.append({'product': product.name, 'location': location.name, 'qty': qty})
    return render_template('report.html', report_data=report_data)

# -------------------------
# Safe DB Initialization
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if not exist
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
