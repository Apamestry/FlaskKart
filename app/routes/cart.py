from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app.extensions import db
from app.models.cart import CartItem
from app.models.product import Product

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route("/")
@login_required
def view_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum((item.subtotal for item in items), start=0)
    return render_template("cart/view.html", items=items, total=total)


@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product is None or not product.is_active:
        abort(404)

    if not product.in_stock():
        flash(f"{product.name} is out of stock.", "warning")
        return redirect(url_for("product.product_detail", product_id=product_id))

    requested_qty = request.form.get("quantity", type=int)
    if requested_qty is None:
        requested_qty = 1
    requested_qty = max(1, requested_qty)

    existing = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if existing:
        new_qty = existing.quantity + requested_qty
        if new_qty > product.stock:
            flash(f"Only {product.stock} of {product.name} available. Cart not updated beyond that.", "warning")
            new_qty = product.stock
        existing.quantity = new_qty
    else:
        qty = min(requested_qty, product.stock)
        db.session.add(CartItem(user_id=current_user.id, product_id=product_id, quantity=qty))

    db.session.commit()
    flash(f"{product.name} added to cart.", "success")
    return redirect(url_for("product.product_detail", product_id=product_id))


@cart_bp.route("/update/<int:item_id>", methods=["POST"])
@login_required
def update_quantity(item_id):
    item = CartItem.query.get(item_id)
    if item is None or item.user_id != current_user.id:
        abort(404)

    new_qty = request.form.get("quantity", type=int)
    if new_qty is None:
        new_qty = 1

    if new_qty < 1:
        db.session.delete(item)
        db.session.commit()
        flash("Item removed from cart.", "info")
        return redirect(url_for("cart.view_cart"))

    if new_qty > item.product.stock:
        new_qty = item.product.stock
        flash(f"Only {item.product.stock} of {item.product.name} available.", "warning")

    item.quantity = new_qty
    db.session.commit()
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get(item_id)
    if item is None or item.user_id != current_user.id:
        abort(404)

    db.session.delete(item)
    db.session.commit()
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart.view_cart"))