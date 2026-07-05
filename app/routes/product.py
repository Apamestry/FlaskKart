from flask import Blueprint, render_template, abort, request

from app.extensions import db
from app.models.product import Product

product_bp = Blueprint("product", __name__, url_prefix="/products")


@product_bp.route("/")
def list_products():
    query = Product.query.filter_by(is_active=True)

    search_term = request.args.get("q", "").strip()
    if search_term:
        query = query.filter(Product.name.ilike(f"%{search_term}%"))

    category = request.args.get("category", "").strip()
    if category:
        query = query.filter(Product.category == category)

    products = query.order_by(Product.created_at.desc()).all()

    # Distinct categories among active products, for the filter dropdown
    categories = [
        row[0] for row in
        db.session.query(Product.category).filter_by(is_active=True).distinct().order_by(Product.category).all()
    ]

    return render_template(
        "products/list.html",
        products=products,
        categories=categories,
        search_term=search_term,
        selected_category=category,
    )


@product_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get(product_id)
    if product is None or not product.is_active:
        abort(404)
    return render_template("products/detail.html", product=product)