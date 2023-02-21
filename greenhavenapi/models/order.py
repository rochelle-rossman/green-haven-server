from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .user import User
from .payment_method import PaymentMethod

class Order(models.Model):
    STATUS_CHOICES = (
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_on = models.DateField(auto_now_add=True, null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField("Product", through="ProductOrder", related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in-progress')
    
    def total(self):
        """This method calculates and returns the total cost of all products in the order."""
        total = 0
        for product in self.products.all():
            total += product.price
        return total
    
@receiver(pre_save, sender=Order)
def set_ordered_on_to_null(instance, **kwargs):
    """When an order is created, status is set to null and ordered_on is null until staus is changed"""
    if instance.status == 'in-progress':
        instance.ordered_on = None
pre_save.connect(set_ordered_on_to_null, sender=Order)
