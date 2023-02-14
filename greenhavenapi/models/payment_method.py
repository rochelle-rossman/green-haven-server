import re
from django.core.exceptions import ValidationError
from django.db import models
from .user import User

def validate_card_number(value):
    """Validate credit card number"""
    if not re.match(r'^[0-9]{16}$', value):
        raise ValidationError('Invalid credit card number format. Use 16 digits')
      
def validate_expiration_date(value):
    """Validates the expiration date format
"""
    if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{2}$', value):
        raise ValidationError('Invalid expiration date format. Use MM/YY')


class PaymentMethod(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=25)
    card_number = models.CharField(max_length=16, validators=[validate_card_number])
    expiration_date = models.CharField(max_length=5, validators=[validate_expiration_date])
