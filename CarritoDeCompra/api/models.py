from django.db import models
from django.utils import timezone

# Create your models here.


class Gorras(models.Model):
    color_princpal= models.CharField(max_length=50)
    color_segundaria= models.CharField(max_length=50)
    color_logo=models.CharField(max_length=50)
    stock_initial= models.PositiveIntegerField()
    descripcion=models.TextField(max_length=500)
    price= models.FloatField(default=0)
    creado = models.DateTimeField(auto_now=False, auto_now_add=False,default=timezone.now)
    imagen=models.URLField(null=True,blank=True,default="https://placehold.co/600x400/png")
    class Meta:
        ordering=["creado"]

class Tejido(models.Model):
    typo_tejido=models.CharField(max_length=90)
    def __str__(self) -> str:
        return self.typo_tejido

class Camiseta(models.Model):
    
    color_principal= models.CharField(max_length=50)
    color_segundaria= models.CharField(max_length=50)
    talla= models.CharField(max_length=50)
    marca= models.CharField(max_length=50)
    genero= models.CharField(max_length=50)
    con_mangas=models.BooleanField()
    stock_initial= models.PositiveIntegerField()
    descripcion=models.TextField(max_length=9999)
    creado = models.DateTimeField(auto_now=False, auto_now_add=False,default=timezone.now)
    price= models.FloatField(default=0)
    typo_tejido=models.ForeignKey(Tejido,on_delete=models.CASCADE,default=None)
    imagen=models.URLField(null=True,blank=True,default="https://placehold.co/600x400/png")
    class Meta:
        ordering=["creado"]


class CartItem(models.Model):
    gorras = models.ForeignKey(Gorras, on_delete=models.CASCADE)
    camiseta=models.ForeignKey(Camiseta,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    





    





