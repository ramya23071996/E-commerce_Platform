from flask import Blueprint, render_template
from models import Product

products_bp = Blueprint("products_bp", __name__)

@products_bp.route("/products")
def view_products():
    products = Product.query.all()
    return render_template("products.html", products=products)