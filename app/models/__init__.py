# Import model modules here as they're added, so Flask-Migrate can see them.
from app.models.user import User  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.cart import CartItem  # noqa: F401
from app.models.order import Order  # noqa: F401
from app.models.order_item import OrderItem  # noqa: F401