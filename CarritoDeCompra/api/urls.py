
# urls.py

from django.urls import path,include
from .views import CombinedListView,GetRoutes,CamisetaCrud
from rest_framework.routers import DefaultRouter



urlpatterns = [
    
    path('listado',CombinedListView.as_view(), name='listado'),
    path('', GetRoutes.as_view(), name='get_routes'),
    path("crud/<int:pk>", CamisetaCrud.as_view())
    
]
