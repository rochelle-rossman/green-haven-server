from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = (
      ('houseplant', 'Houseplant'),
      ('home_decor', 'Home/Decor'),
      ('plant_care', "Plant Care"),
      ('planters_stands', 'Planters/Stands'),
    )
    name = models.CharField(max_length=30)
    image_url = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(99999.99)])
    inventory = models.IntegerField()
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)

    def __str__(self):
        return self.name
      
    def deduct_from_inventory(self, quantity):
        """Deducts quantity from inventory value when product is added to an order."""
        if self.inventory >= quantity:
            self.inventory -= quantity
            self.save()
        else:
            raise ValueError("Not enough inventory to complete the order.")


class Houseplant(Product):
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
    light_level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    water_needs = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    care_level = models.CharField(max_length=20, choices=CARE_CHOICES)
    pet_friendly = models.BooleanField(default=False)

    def clean(self):
        if self.product_type != 'houseplant':
            raise ValidationError("Houseplant objects must have a product_type of 'houseplant'.")

    def __str__(self):
        return f"{self.name} (Houseplant)"

class HomeDecor(Product):
    STYLE_CHOICES = (
      ('modern', 'Modern'),
      ('industrial', 'Industrial'),
      ('bohemian', 'Bohemian'),
      ('farmhouse', 'Farmhouse'),
      ('traditional', 'Traditional'),
      ('midcentury_modern', 'Midcentury Modern'),
    )
    style = models.CharField(max_length=20, choices=STYLE_CHOICES)
    
    def __str__(self):
        return f"{self.name} (Home/Decor)"
    def clean(self):
        if self.name != 'home_decor':
            raise ValidationError("Home/Decor object must have a product_type of 'home_decor'.")
