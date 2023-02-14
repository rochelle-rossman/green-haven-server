from django.db import models
from .product import Product
from .design import Design

class ProductDesign(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
