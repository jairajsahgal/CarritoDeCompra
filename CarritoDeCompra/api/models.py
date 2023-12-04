from django.db import models
from django.utils import timezone


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


class Gorras(Product):
    # * Caps Model
    logo_color = models.CharField(max_length=50)

    class Meta:
        ordering = ["created_at"]


class Tejido(models.Model):
    # * Model for Tissue
    typo_tejido = models.CharField(max_length=90)

    def __str__(self) -> str:
        return self.typo_tejido


class Camiseta(models.Model):
    # * Model for Tshirt
    size_specification = models.CharField(
        max_length=10,
        choices=[("MEN", "Men"), ("WOMEN", "Women"), ("UNISEX", "Unisex")],
    )
    sleeveless = models.BooleanField()
    typo_tejido = models.ForeignKey(Tejido, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ["created_at"]


class CartItem(models.Model):
    gorras = models.ForeignKey(Gorras, on_delete=models.CASCADE)
    camiseta = models.ForeignKey(Camiseta, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
