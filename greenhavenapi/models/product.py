from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .product_type import ProductType

class Product(models.Model):
    CARE_CHOICES = (
      ('novice', 'Novice'),
      ('intermediate', 'Intermediate'),
      ('expert', 'Expert'),
    )
    LEVEL_CHOICES = (
      ('low', 'Low'),
      ('medium', 'Medium'),
      ('high', 'High'),
    )
    STYLE_CHOICES = (
      ('modern', 'Modern'),
      ('industrial', 'Industrial'),
      ('bohemian', 'Bohemian'),
      ('farmhouse', 'Farmhouse'),
      ('traditional', 'Traditional'),
      ('midcentury_modern', 'Midcentury Modern'),
    )
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(99999.99)])
    inventory = models.IntegerField()
    product_type = models.ManyToManyField(ProductType)
    light_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, null=True)
    water_needs = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, null=True)
    care_level = models.CharField(max_length=20, choices=CARE_CHOICES, blank=True, null=True)
    pet_friendly = models.BooleanField(blank=True, null=True)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name
      
    def deduct_from_inventory(self, quantity):
        """Deducts quantity from inventory value when product is added to an order."""
        if self.inventory >= quantity:
            self.inventory -= quantity
            self.save()
        else:
            raise ValueError("Not enough inventory to complete the order.")
