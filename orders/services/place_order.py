from orders.models import Products, Orders
from django.db import transaction
from django.contrib.auth.models import User

class PlaceOrder(object):
    def __init__(self, user_id, orders):
        self.user_id = user_id
        self.orders = orders
    
    def get_product_by_name(self, name):
        try:
            product = Products.objects.get(product_name=name)
        except Products.DoesNotExist:
            product = None
        return product
    
    def perform_task(self):
        with transaction.atomic():
            unavailable_items = []
            valid_orders = []
            user = User.objects.get(pk=self.user_id)
            for order in self.orders:
                product = self.get_product_by_name(order['product_name'])
                if product:
                    if order['quantity'] > product.available_quantity:
                        order.update({"available_quantity":product.available_quantity})
                        unavailable_items.append(dict(order))
                    else:
                        valid_orders.append(Orders(**{
                            "user": user,
                            "product": product,
                            "quantity": order['quantity'],
                            "price": product.price,
                        }))
                else:
                    order.update({"available_quantity":0})
                    unavailable_items.append(dict(order))
            if not unavailable_items:
                Orders.objects.bulk_create(valid_orders)
                for order in valid_orders:
                    product = order.product
                    product.available_quantity = product.available_quantity - order.quantity
                    product.save()
                return {"result": "success", "message": "order placed successfully"}
            return {"result":"error", "message": f"Items unavailable - {unavailable_items}"}