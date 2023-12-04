from rest_framework import serializers
from .models import Camiseta, Gorras, Tejido
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class TejidoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tejido
        fields = "__all__"


class GorrasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gorras
        exclude = ("initial_stock",)


class CamisetaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Camiseta
        exclude = ("initial_stock",)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], None, validated_data["password"]
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")
