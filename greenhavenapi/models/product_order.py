from django.db import models
from .product import Product
from .order import Order

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    # This method overrides the default `save` method and calls the parent class's save method first
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.deduct_from_inventory(self.quantity)
        
    def delete(self, *args, **kwargs):
      # Update the product's inventory before deleting the order
        self.update_inventory_on_delete(self)
        super().delete(*args, **kwargs)
        
    @staticmethod
    def update_inventory_on_delete(product_order):
        """updates the inventory of the product associated with the product 
        order that's being deleted then adds the quantity of the product back to the inventory."""
        # Get the product associated with this order
        product = product_order.product
        # Increment the product's inventory by the quantity of this order
        product.inventory += product_order.quantity
        # Save the product object to persist the change
        product.save()
