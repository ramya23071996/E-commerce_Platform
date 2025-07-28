from flask import Blueprint, session, redirect, url_for, request, render_template
from models import Product

cart_bp = Blueprint("cart_bp", __name__)

@cart_bp.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(pid)
        if product:
            subtotal = qty * product.price
            total += subtotal
            items.append({"product": product, "qty": qty, "subtotal": subtotal})
    return render_template("cart.html", items=items, total=total)

@cart_bp.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("products_bp.view_products"))

@cart_bp.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for("cart_bp.view_cart"))