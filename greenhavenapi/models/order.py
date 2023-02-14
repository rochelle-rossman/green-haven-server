from django.db import models
from .user import User
from .payment_method import PaymentMethod

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_on = models.DateField(auto_now_add=True, null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField("Product", through="ProductOrder", related_name="orders")
    def total(self):
        """This method calculates and returns the total cost of all products in the order."""
        total = 0
        for product in self.products.all():
            total += product.price
        return total
