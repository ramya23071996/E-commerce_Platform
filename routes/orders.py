class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    total_price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    items = db.relationship("OrderItem", backref="order")

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)
    price_at_purchase = db.Column(db.Float)

from flask import Blueprint, session, redirect, url_for, render_template
from flask_login import login_required, current_user
from models import db, Product, Order, OrderItem
from datetime import datetime

orders_bp = Blueprint("orders_bp", __name__)

@orders_bp.route("/checkout")
@login_required
def checkout():
    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("cart_bp.view_cart"))

    total = 0
    order = Order(user_id=current_user.id, timestamp=datetime.now())
    db.session.add(order)

    for pid, qty in cart.items():
        product = Product.query.get(pid)
        if product:
            subtotal = product.price * qty
            total += subtotal
            item = OrderItem(order=order, product_id=pid, quantity=qty, price_at_purchase=product.price)
            db.session.add(item)

    order.total_price = total
    db.session.commit()
    session["cart"] = {}
    return render_template("checkout.html", order=order)