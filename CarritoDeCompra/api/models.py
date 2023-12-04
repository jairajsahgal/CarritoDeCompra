from django.db import models
from django.utils import timezone
from api.manager import AppManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


# Create your models here.
class TimeBasedStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(TimeBasedStampModel):
    main_color = models.CharField(max_length=50)
    secondary_color = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    inclusion_date = models.DateField()
    product_photo_url = models.URLField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    initial_stock = models.PositiveIntegerField(editable=False)
    current_stock = models.PositiveIntegerField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    objects = AppManager


class Gorras(Product):
    # * Caps Model
    logo_color = models.CharField(max_length=50)


class Tejido(models.Model):
    # * Model for Tissue
    typo_tejido = models.CharField(max_length=90)

    def __str__(self) -> str:
        return self.typo_tejido


class Camiseta(Product):
    # * Model for Tshirt
    size_specification = models.CharField(
        max_length=10,
        choices=[("MEN", "Men"), ("WOMEN", "Women"), ("UNISEX", "Unisex")],
    )
    sleeveless = models.BooleanField()
    typo_tejido = models.ForeignKey(Tejido, on_delete=models.CASCADE, default=None)


class Cart(TimeBasedStampModel):
    date = models.DateField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # Generic relationship to a product (e.g., cap or t-shirt)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.quantity} of {self.product.__class__.__name__} (ID: {self.product.id})"
