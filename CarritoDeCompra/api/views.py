from operator import is_
from re import search
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets, status
from api.models import Cart, CartItem, Gorras, Camiseta, Product
from api.serializer import (
    CamisetaSerializers,
    GorrasSerializers,
    CreateUserSerializer,
    UserSerializer,
    LoginUserSerializer,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from itertools import chain
from knox.models import AuthToken
from rest_framework import permissions
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
import json
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


class GorrasModelViewSet(viewsets.ModelViewSet):
    queryset = Gorras.objects.all().exclude(is_deleted=True)
    serializer_class = GorrasSerializers
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = "__all__"
    ordering = ["-created_at"]
    search_fields = ["main_color", "secondary_color", "brand", "logo_color"]


class CamisetaModelViewSet(viewsets.ModelViewSet):
    queryset = Camiseta.objects.all().exclude(is_deleted=True)
    serializer_class = CamisetaSerializers
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = "__all__"
    ordering = ["-created_at"]
    search_fields = [
        "name",
        "size_specification",
        "sleeveless",
        "main_color",
        "secondary_color",
        "brand",
    ]


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Cart, CartItem
from django.utils import timezone


@require_GET
def get_todays_cart_items(request):
    # Get today's date
    today = timezone.localdate()

    # Try to retrieve the cart for today
    cart, created = Cart.objects.get_or_create(date=today, is_completed=False)
    if created:
        cart.save()
        return JsonResponse({"message": "No cart items for today"}, status=200)

    # Gather all cart items for the current cart
    cart_items = cart.items.all()

    # Prepare the data for JSON serialization
    cart_items_data = []
    for item in cart_items:
        product = item.product

        # Build the product data including checking if it's soft-deleted
        product_data = {
            "id": product.id,
            "product_photo_url": product.product_photo_url,
            "unit_price": product.unit_price,
            "description": product.description,
        }

        cart_items_data.append(
            {
                "item_id": item.id,
                "quantity": item.quantity,
                "product": product_data,
            }
        )

    return JsonResponse({"cart_id": cart.id, "items": cart_items_data}, safe=False)


# Helper function to resolve GenericForeignKey relation
def generic_relation_to_product(product_instance):
    content_type = ContentType.objects.get_for_model(product_instance)
    return {"content_type": content_type, "object_id": product_instance.pk}


@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        # Parse request data
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            quantity = int(data.get("quantity", 1))
            product_type = data.get("product_type", "").lower()

            if not product_type or not product_id:
                return HttpResponseBadRequest("Product type and id required")

        except ValueError:
            return HttpResponseBadRequest("Invalid JSON")

        # Check product availability and stock
        product_model = Gorras if product_type == "gorras" else Camiseta
        product = get_object_or_404(product_model, pk=product_id)
        if product.is_deleted or product.current_stock < quantity:
            return HttpResponseBadRequest("Product not available or insufficient stock")

        # Retrieve or create the cart
        today = timezone.localdate()
        cart, created = Cart.objects.get_or_create(date=today)
        # Add or update the cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=generic_relation_to_product(product),
            defaults={"quantity": quantity},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Decrease the product stock
        product.current_stock -= quantity
        product.save()

        # Send success response including the cart item details
        return JsonResponse(
            {
                "success": True,
                "item_id": cart_item.id,
                "quantity": cart_item.quantity,
                "product_id": product.id,
                "product_type": product.__class__.__name__,
                "new_stock": product.current_stock,
            },
            status=201,
        )

    else:
        return HttpResponseBadRequest("Only POST requests are allowed")


@csrf_exempt  # Disable CSRF for demonstration purposes.
def purchase(request):
    if request.method == "POST":
        # Parse and validate request data
        try:
            data = json.loads(request.body)
            customer_name = data.get("name")
            customer_last_name = data.get("last_name")
            postal_address = data.get("postal_address")
            email = data.get("email")
            phone_number = data.get("phone_number")

            if not (
                customer_name
                and customer_last_name
                and postal_address
                and email
                and phone_number
            ):
                return HttpResponseBadRequest("All fields are required")

        except ValueError:
            return HttpResponseBadRequest("Invalid JSON")

        # Retrieve the cart for today
        today = timezone.localdate()
        cart = Cart.objects.filter(date=today, is_completed=False).first()
        if not cart:
            return HttpResponseBadRequest("No pending cart for today")

        # Simulate purchase by updating the cart's purchased status
        cart.is_completed = True
        cart.save()

        # Prepare email content with purchase summary
        cart_items = CartItem.objects.filter(cart=cart)
        purchase_summary = "\n".join(
            [
                f"{item.quantity}x {item.product.__class__.__name__} (ID: {item.product.id})"
                for item in cart_items
            ]
        )

        message = (
            f"Thank you for your purchase, {customer_name}!\n\n"
            "Purchase summary:\n"
            f"{purchase_summary}\n\n"
            "We will ship your items to {postal_address}."
        )

        # Send email to the customer
        send_mail(
            subject="Your Purchase Summary",
            message=message,
            from_email=settings.DEFAULT_EMAIL,  # Use your actual email address
            recipient_list=[email],
            fail_silently=False,
        )

        # Respond to the request indicating success
        return JsonResponse(
            {"success": True, "message": "Purchase completed and email sent"},
            status=200,
        )

    else:
        return HttpResponseBadRequest("Only POST requests are allowed")
