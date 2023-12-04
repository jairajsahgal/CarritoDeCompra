# urls.py

from django.urls import path, include
from api.views import (
    CamisetaModelViewSet,
    GorrasModelViewSet,
    RegistrationAPI,
    LoginAPI,
    UserAPI,
    get_todays_cart_items,
    add_to_cart,
    purchase,
)
from knox.views import LogoutAllView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"camiseta",
    CamisetaModelViewSet,
    basename="camiseta",
)
router.register(r"gorras", GorrasModelViewSet, basename="gorras")


urlpatterns = router.urls
urlpatterns += [
    path("register/", RegistrationAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("logout/", LogoutAllView.as_view(), name="knox_logoutall"),
    path("user_detail", UserAPI.as_view(), name="user_detail"),
    path("todays_cart_items/", get_todays_cart_items, name="todays_cart_items"),
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path("purchase", purchase, name="purchase"),
]
