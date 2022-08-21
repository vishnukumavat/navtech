from orders.models import Products

class CreateOrUpdateProducts(object):
    def __init__(self, productList):
        self.productList = productList
    
    def valid_product(self, product):
        return all([
            isinstance(product['product_name'], str), 
            str(product['price']).isnumeric(), 
            str(product['available_quantity']).isnumeric(), 
        ])

    
    def perform_task(self):
        rejected_items = []
        for item in self.productList:
            if self.valid_product(item):
                product, created = Products.objects.get_or_create(product_name=item['product_name'])
                product.price = item['price']
                if created:
                    product.available_quantity = item['available_quantity']
                else:
                    product.available_quantity = product.available_quantity + int(item['available_quantity'])
                product.save()
            else:
                rejected_items.append(item)
        return {"rejected_items": rejected_items}