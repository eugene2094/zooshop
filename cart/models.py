from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from shop.models import Product  # замените на вашу модель товара


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity
