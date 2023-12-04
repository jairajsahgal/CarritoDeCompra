from rest_framework import serializers
from .models import Camiseta,Gorras,Tejido

class TejidoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Tejido
        fields="__all__"


class GorrasSerializers(serializers.ModelSerializer):
    class Meta:
        model=Gorras
        
        exclude = ['stock_initial'] 

class CamisetaSerializers(serializers.ModelSerializer):
    class Meta:
        model=Camiseta
        exclude = ['stock_initial'] 
        
    def create(self, validated_data):
        typo_tejido_data =validated_data.pop("typo_tejido")
        typo_tejido = Tejido.objects.create(**typo_tejido_data)
        camiseta = Camiseta.objects.create(typo_tejido=typo_tejido, **validated_data)
        return camiseta
    