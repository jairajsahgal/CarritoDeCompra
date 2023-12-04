from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics,viewsets,status
from .models import Gorras,Camiseta
from .serializer import CamisetaSerializers, GorrasSerializers
# Create your views here.

class GetRoutes(APIView):
    def get (self, request):
        routes=[{
            "Get":"/api/list"
        }]
        return Response(routes)


class CombinedListView(APIView):
    def get(self,request,*arg,**kwargs):
        camisetas = Camiseta.objects.all()
        gorras = Gorras.objects.all()

        camiseta_serializer = CamisetaSerializers(camisetas, many=True)
        gorras_serializer = GorrasSerializers(gorras, many=True)

        combined_data = {
            'gorras': gorras_serializer.data,
            'camisetas': camiseta_serializer.data
            
        }

        return Response(combined_data, status=status.HTTP_200_OK)

# class CamisetaCrud(APIView):
#     def get(self,request,pk):
#         camiseta_data=request.data
#         id=camiseta_data.get("id",None)
#         if id is not None:
#             camiseta_obj = get_object_or_404(Camiseta, pk=pk)
#             camiseta_seri = CamisetaSerializers(camiseta_obj)
#             return Response(camiseta_seri.data)
#         camiseta_obj=Camiseta.objects.all()
#         camiseta_seri=CamisetaSerializers(camiseta_obj,many=True)
        
#         return Response(camiseta_seri.data)

#     def post(self,request):
#         camiseta_data=request.data
#         camiseta_seri=CamisetaSerializers(data=camiseta_data)
#         if camiseta_seri.is_valid():
#             camiseta_seri.save()
#             return Response(camiseta_seri.data)
#         else :
#             return Response(camiseta_seri.errors)

#     def put(self,request):
#         camiseta_data = request.data
#         id = camiseta_data.get("id", None)
#         try:
#             camiseta_obj = Camiseta.objects.get(id=id)
#         except Camiseta.DoesNotExist:
#             raise Http404("Camiseta not found 404 ")
#         camiseta_seri = CamisetaSerializers(
#             camiseta_obj, data=camiseta_data, partial=True)
#         if camiseta_seri.is_valid():
#             camiseta_seri.save()
#             return Response(camiseta_seri.data)
#         else:
#             return Response(camiseta_seri.errors)
#     def delete(self,request):
#         camiseta_data = request.data
#         id = camiseta_data.get("id", None)
#         try:
#             camiseta_obj = Camiseta.objects.get(id=id)
#         except Camiseta.DoesNotExist:
#             response = {
#                 "msg": f"There is no such student model with this id {id}"
#             }
#             return Response(response)
            
#         camiseta_obj.delete()
#         response = {
#             "msg": "your data has beeen deletedddddd...."
#         }
#         return Response(response)

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Camiseta
from .serializer import CamisetaSerializers

class CamisetaCrud(APIView):
    def get(self, request, pk):
        camiseta_obj = get_object_or_404(Camiseta, pk=pk)
        camiseta_seri = CamisetaSerializers(camiseta_obj)
        return Response(camiseta_seri.data)

    def post(self, request):
        camiseta_seri = CamisetaSerializers(data=request.data)
        if camiseta_seri.is_valid():
            camiseta_seri.save()
            return Response(camiseta_seri.data, status=status.HTTP_201_CREATED)
        else:
            return Response(camiseta_seri.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        camiseta_obj = get_object_or_404(Camiseta, pk=pk)
        camiseta_seri = CamisetaSerializers(camiseta_obj, data=request.data, partial=True)
        if camiseta_seri.is_valid():
            camiseta_seri.save()
            return Response(camiseta_seri.data)
        else:
            return Response(camiseta_seri.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        camiseta_obj = get_object_or_404(Camiseta, pk=pk)
        camiseta_obj.delete()
        response = {"msg": f"Camiseta with id {pk} has been deleted."}
        return Response(response, status=status.HTTP_204_NO_CONTENT)



    



