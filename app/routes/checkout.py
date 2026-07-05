from flask import Blueprint, render_template, redirect, url_for, flash, session, abort
from flask_login import login_required, current_user

from app.extensions import db
from app.models.cart import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.forms.checkout_forms import ShippingForm

checkout_bp = Blueprint("checkout", __name__, url_prefix="/checkout")


def _get_cart_items_and_total():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum((item.subtotal for item in items), start=0)
    return items, total


@checkout_bp.route("/shipping", methods=["GET", "POST"])
@login_required
def shipping():
    items, total = _get_cart_items_and_total()
    if not items:
        flash("Your cart is empty. Add something before checking out.", "warning")
        return redirect(url_for("cart.view_cart"))

    form = ShippingForm()

    if not form.is_submitted() and session.get("shipping_info"):
        form.process(data=session["shipping_info"])

    if form.validate_on_submit():
        session["shipping_info"] = {
            "full_name": form.full_name.data.strip(),
            "address_line1": form.address_line1.data.strip(),
            "address_line2": form.address_line2.data.strip(),
            "city": form.city.data.strip(),
            "state": form.state.data.strip(),
            "zip_code": form.zip_code.data.strip(),
            "phone": form.phone.data.strip(),
        }
        return redirect(url_for("checkout.review"))

    return render_template("checkout/shipping.html", form=form)


@checkout_bp.route("/review")
@login_required
def review():
    items, total = _get_cart_items_and_total()
    if not items:
        flash("Your cart is empty. Add something before checking out.", "warning")
        return redirect(url_for("cart.view_cart"))

    shipping_info = session.get("shipping_info")
    if not shipping_info:
        flash("Please enter your shipping details first.", "info")
        return redirect(url_for("checkout.shipping"))

    return render_template(
        "checkout/review.html", items=items, total=total, shipping=shipping_info
    )


@checkout_bp.route("/place-order", methods=["POST"])
@login_required
def place_order():
    items, total = _get_cart_items_and_total()
    if not items:
        flash("Your cart is empty. Add something before checking out.", "warning")
        return redirect(url_for("cart.view_cart"))

    shipping_info = session.get("shipping_info")
    if not shipping_info:
        flash("Please enter your shipping details first.", "info")
        return redirect(url_for("checkout.shipping"))

    for item in items:
        if item.quantity > item.product.stock:
            flash(
                f"Sorry, only {item.product.stock} of {item.product.name} is available now. "
                "Please update your cart.",
                "danger",
            )
            return redirect(url_for("cart.view_cart"))

    order = Order(
        user_id=current_user.id,
        total_amount=total,
        payment_status="Completed",
        order_status="Placed",
        shipping_full_name=shipping_info["full_name"],
        shipping_address_line1=shipping_info["address_line1"],
        shipping_address_line2=shipping_info.get("address_line2") or None,
        shipping_city=shipping_info["city"],
        shipping_state=shipping_info["state"],
        shipping_zip_code=shipping_info["zip_code"],
        shipping_phone=shipping_info["phone"],
    )
    db.session.add(order)
    db.session.flush()

    for item in items:
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            product_name=item.product.name,
            price_at_purchase=item.product.price,
            quantity=item.quantity,
        ))
        item.product.stock -= item.quantity
        db.session.delete(item)

    db.session.commit()
    session.pop("shipping_info", None)

    return redirect(url_for("checkout.success", order_id=order.id))


@checkout_bp.route("/success/<int:order_id>")
@login_required
def success(order_id):
    order = Order.query.get(order_id)
    if order is None or order.user_id != current_user.id:
        abort(404)
    return render_template("checkout/success.html", order=order)