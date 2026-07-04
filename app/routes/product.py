from flask import Blueprint, render_template, abort

from app.models.product import Product

product_bp = Blueprint("product", __name__, url_prefix="/products")


@product_bp.route("/")
def list_products():
    products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()
    return render_template("products/list.html", products=products)


@product_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get(product_id)
    if product is None or not product.is_active:
        abort(404)
    return render_template("products/detail.html", product=product)