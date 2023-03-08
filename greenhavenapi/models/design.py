from django.db import models

class Design(models.Model):
    ROOM_CHOICES = (
      ('living_room', 'Living Room'),
      ('bedroom', 'Bedroom'),
      ('office', 'Office'),
      ('bathroom', 'Bathroom')
    )
    STYLE_CHOICES = (
      ('modern', 'Modern'),
      ('industrial', 'Industrial'),
      ('bohemian', 'Bohemian'),
      ('farmhouse', 'Farmhouse'),
      ('traditional', 'Traditional'),
      ('midcentury_modern', 'Midcentury Modern'),
    )
    room = models.CharField(max_length=15, choices=ROOM_CHOICES)
    style = models.CharField(max_length=25, choices=STYLE_CHOICES)
    image_url = models.CharField(max_length=100)
    products = models.ManyToManyField("Product", through="ProductDesign")
    description = models.CharField(max_length=1000, default="", blank=True)
